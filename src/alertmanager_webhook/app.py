import asyncio

from .alertmanager import Alertmanager
from .config import Config
from .slack import Slack
from .state import State
from .web import WebApp


async def app(config: Config) -> None:
    slack = Slack(config.slack)

    am = Alertmanager.from_config(config)
    state = State(am)

    webapp = WebApp(config, slack, state)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(state.keep_fresh())
        tg.create_task(webapp.serve())
