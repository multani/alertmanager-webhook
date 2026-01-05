import re
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator
from typing import Self

from httpx import AsyncClient
from pydantic import BaseModel
from pydantic import Field
from pydantic import RootModel

from .config import Config
from .models import Alert
from .models import AlertPayload


class SilenceStatus(BaseModel):
    # "expired", "active", "pending"]
    state: str  # active


class SilenceMatcher(BaseModel):
    is_equal: bool = Field(alias="isEqual")
    is_regex: bool = Field(alias="isRegex")
    name: str
    value: str

    def match(self, alert: Alert) -> bool:
        labels = alert.labels

        if self.name not in labels:
            return False

        value = labels[self.name]

        if self.is_equal:
            return value == self.value

        # regex
        return re.match(self.value, value) is not None


# https://github.com/prometheus/alertmanager/blob/main/api/v2/openapi.yaml
class Silence(BaseModel):
    id: str

    starts_at: datetime = Field(alias="startsAt")
    updated_at: datetime = Field(alias="updatedAt")
    ends_at: datetime = Field(alias="endsAt")

    comment: str
    created_by: str = Field(alias="createdBy")
    status: SilenceStatus

    matchers: list[SilenceMatcher]

    def match(self, alerts: AlertPayload) -> bool:
        for alert in alerts.alerts:
            if self.match_alert(alert):
                return True

        return False

    def match_alert(self, alert: Alert) -> bool:
        for matcher in self.matchers:
            if not matcher.match(alert):
                return False

        return True


class Silences(RootModel[list[Silence]]):
    def __iter__(self) -> Iterator[Silence]:  # type: ignore[override]
        return iter(self.root)

    def __len__(self) -> int:
        return len(self.root)


@dataclass
class Alertmanager:
    client: AsyncClient

    @classmethod
    def from_config(cls, config: Config) -> Self:
        client = AsyncClient(base_url=config.alertmanager.url)
        return cls(client=client)

    async def get_silences(self) -> Silences:
        response = await self.client.get("/api/v2/silences")
        response.raise_for_status()

        data = response.text
        silences = Silences.model_validate_json(data)

        return silences
