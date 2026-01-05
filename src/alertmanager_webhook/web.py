import contextlib
from dataclasses import dataclass
from typing import AsyncIterator
from typing import TypedDict

import pydantic
import uvicorn
from prometheus_client import make_asgi_app
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.responses import Response
from starlette.routing import Route

from .config import Config
from .models import AlertPayload
from .slack import Slack
from .state import State
from .utils import json_printer


async def alerts_handler(request: Request) -> Response:
    body = await request.body()
    try:
        alert = AlertPayload.model_validate_json(body)
    except pydantic.ValidationError:
        return PlainTextResponse("invalid", status_code=400)

    slack = request.state.slack
    state: State = request.state.state

    for silence in state.silences:
        if silence.match(alert):
            print("Alert is / was silenced")
            break

    await slack.send_message("#alerts", alert)

    # Print back the body if it's a valid alert payload
    json_printer(body)
    return PlainTextResponse("ok")


class RequestState(TypedDict):
    slack: Slack
    state: State


@dataclass
class WebApp:
    slack: Slack
    state: State
    app: Starlette

    uvicorn_config: uvicorn.Config

    def __init__(self, config: Config, slack: Slack, state: State) -> None:
        routes = [
            Route("/alerts/handle", alerts_handler, methods=["POST"]),
        ]

        self.app = Starlette(
            lifespan=self.lifespan,
            routes=routes,
        )

        # Serve Prometheus metrics at /metrics
        metrics_app = make_asgi_app()
        self.app.mount("/metrics", metrics_app)

        self.uvicorn_config = uvicorn.Config(
            self.app,
            host="0.0.0.0",
            port=config.web.port,
            log_level="info",
        )

        self.slack = slack
        self.state = state

    @contextlib.asynccontextmanager
    async def lifespan(self, app: Starlette) -> AsyncIterator[RequestState]:
        """Attach the state of the application to each request."""
        yield RequestState(slack=self.slack, state=self.state)

    async def serve(self) -> None:
        server = uvicorn.Server(self.uvicorn_config)
        await server.serve()
