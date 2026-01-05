from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from pydantic import Field


# https://prometheus.io/docs/alerting/latest/configuration/#webhook_config
class Alert(BaseModel):
    status: str
    labels: dict[str, str]
    annotations: dict[str, str]
    starts_at: datetime = Field(alias="startsAt")
    ends_at: datetime = Field(alias="startsAt")

    generator_url: str = Field(alias="generatorURL")
    "identifies the entity that caused the alert"

    fingerprint: str
    "fingerprint to identify the alert"


# https://prometheus.io/docs/alerting/latest/configuration/#webhook_config
class AlertPayload(BaseModel):
    version: Literal["4"]

    group_key: str = Field(alias="groupKey")
    "key identifying the group of alerts (e.g. to deduplicate)"

    truncated_alerts: int = Field(alias="truncatedAlerts")
    "how many alerts have been truncated due to `max_alerts`"

    status: str
    receiver: str

    group_labels: dict[str, str] = Field(alias="groupLabels")
    common_labels: dict[str, str] = Field(alias="commonLabels")
    common_annotations: dict[str, str] = Field(alias="commonAnnotations")

    external_url: str = Field(alias="externalURL")
    "backlink to the Alertmanager."

    alerts: list[Alert] = []
