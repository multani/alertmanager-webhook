from pathlib import Path
from typing import Self

import yaml
from pydantic import BaseModel


class SlackConfig(BaseModel):
    token: str


class WebConfig(BaseModel):
    port: int = 5000


class AlertmanagerConfig(BaseModel):
    url: str = "http://localhost:19091"


class Config(BaseModel):
    slack: SlackConfig
    web: WebConfig
    alertmanager: AlertmanagerConfig

    @classmethod
    def load(cls, file: Path) -> Self:
        data = yaml.safe_load(file.read_text())
        return cls.model_validate(data)
