import asyncio
from dataclasses import dataclass
from dataclasses import field

import structlog

from .alertmanager import Alertmanager
from .alertmanager import Silences

logger = structlog.get_logger(__name__)


@dataclass
class State:
    alertmanager: Alertmanager
    silences: Silences = field(default_factory=lambda: Silences([]))

    async def refresh(self) -> None:
        logger.info("Refreshing silences from Alertmanager")
        self.silences = await self.alertmanager.get_silences()
        logger.debug(f"Found {len(self.silences)} silences")

    async def keep_fresh(self) -> None:
        while True:
            await self.refresh()
            await asyncio.sleep(6)
