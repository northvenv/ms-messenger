import os
import logging
import tomllib
from pathlib import Path
from dataclasses import dataclass
from typing import Any

from message_service.infrastructure.persistence.config import (
    MongoDBConfig,
    Collections
)
def load_config_by_path(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with config_path.open("rb") as cfg:
        return tomllib.load(cfg)


@dataclass
class MessageServiceConfig:
    mongo_db_config: MongoDBConfig


def load_message_service_config() -> MessageServiceConfig:
    mongo_db_config = MongoDBConfig(
        host=os.environ["MONGO_HOST"],
        port=os.environ["MONGO_PORT"],
        username=os.environ["MONGO_USER"],
        password=os.environ["MONGO_PASSWORD"],
        db_name=os.environ["MONGO_DB"],
        collections=Collections(
            chat=os.environ["CHAT_MONGO_COLLECTION"],
            message=os.environ["MESSAGE_MONGO_COLLECTION"]
        ),
    )
    cfg_path = os.environ["CONFIG_PATH"]
    cfg = load_config_by_path(Path(cfg_path))

    return MessageServiceConfig(
        mongo_db_config=mongo_db_config,
    )
