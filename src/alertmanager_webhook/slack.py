from typing import Any

import structlog
from slack_sdk.errors import SlackApiError
from slack_sdk.web.async_client import AsyncWebClient

from .config import SlackConfig
from .models import AlertPayload

logger = structlog.get_logger(__name__)


class Slack:
    def __init__(self, config: SlackConfig) -> None:
        self.client = AsyncWebClient(token=config.token)

    async def send_message(self, channel: str, alert: AlertPayload) -> None:
        message = format_alert(alert)

        try:
            await self.client.chat_postMessage(
                channel=channel,
                blocks=message["blocks"],
            )
        except SlackApiError as exc:
            logger.exception("Unable to send message to Slack", exception=exc)


def format_alert(alert: AlertPayload) -> dict[str, Any]:
    # TODO: move this as configuration file templates
    msg: dict[str, Any] = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*:rotating_light: {alert.common_labels['alertname']}*",
                },
            },
            {
                "type": "table",
                "rows": [
                    [
                        {
                            "type": "rich_text",
                            "elements": [
                                {
                                    "type": "rich_text_section",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "text": "K8s Cluster: ",
                                            "style": {
                                                "bold": True,
                                            },
                                        },
                                        {
                                            "type": "text",
                                            "text": alert.common_labels["environment"],
                                            "style": {
                                                "code": True,
                                            },
                                        },
                                    ],
                                }
                            ],
                        },
                        {
                            "type": "rich_text",
                            "elements": [
                                {
                                    "type": "rich_text_section",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "text": "Project: ",
                                            "style": {
                                                "bold": True,
                                            },
                                        },
                                        {
                                            "type": "text",
                                            "text": "GCP / test123",  # TODO
                                            "style": {
                                                "code": True,
                                            },
                                        },
                                    ],
                                }
                            ],
                        },
                        {
                            "type": "rich_text",
                            "elements": [
                                {
                                    "type": "rich_text_section",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "text": "Severity: ",
                                            "style": {
                                                "bold": True,
                                            },
                                        },
                                        {
                                            "type": "text",
                                            "text": alert.common_labels["severity"],
                                            "style": {
                                                "code": True,
                                            },
                                        },
                                    ],
                                }
                            ],
                        },
                    ],
                ],
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Summary*: " + alert.common_annotations["summary"],
                },
            },
            {
                "type": "rich_text",
                "elements": [
                    # {
                    #     "type": "rich_text_section",
                    #     "elements": [
                    #         {
                    #             "type": "text",
                    #             "text": "Basic bullet list with rich elements\n",
                    #         }
                    #     ],
                    # },
                    {
                        "type": "rich_text_list",
                        "style": "bullet",
                        "indent": 0,
                        "elements": [
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {"type": "emoji", "name": "warning"},
                                    {"type": "text", "text": " "},
                                    {
                                        "type": "text",
                                        "text": alert.common_annotations["summary"],
                                    },
                                ],
                            }
                            for al in alert.alerts
                        ],
                    },
                ],
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": ":no_bell: Silence",
                            "emoji": True,
                        },
                        "style": "danger",
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": ":bar_chart: Grafana",
                            "emoji": True,
                        },
                        "url": "https://google.com",  # TODO
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": ":notebook_with_decorative_cover: Runbook",
                            "emoji": True,
                        },
                        "url": "https://google.com",  # TODO
                    },
                ],
            },
        ]
    }

    return msg
