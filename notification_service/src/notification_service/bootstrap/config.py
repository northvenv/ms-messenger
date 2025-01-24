import os
import tomllib
import logging
from pathlib import Path
from typing import Any
from dataclasses import dataclass
from notification_service.message_broker.config import KafkaConfig
from notification_service.sms_sender.config import SmsConfig


@dataclass
class NotificationServiceConfig:
    kafka: KafkaConfig
    sms: SmsConfig


def load_config_by_path(config_path: Path) -> dict[str, Any]:
    with config_path.open("rb") as cfg:
        return tomllib.load(cfg)


def load_notification_service_config() -> NotificationServiceConfig:
    cfg_path = os.environ["CONFIG_PATH"]
    cfg = load_config_by_path(Path(cfg_path))

    try:
        verification_token_topic = cfg["verification"]["verification_token_topic"]
        sms_result_topic = cfg["verification"]["sms_result_topic"]

    except KeyError:
        logging.fatal("On startup: Error reading config %s", cfg_path)
        raise

    kafka = KafkaConfig(
        url=os.environ["KAFKA_URL"],
        verification_token_topic=verification_token_topic,
        sms_result_topic=sms_result_topic
    )

    sms = SmsConfig(
        email=os.environ["SMS_EMAIL"],
        api_key=os.environ["SMS_API_KEY"],
    )
    
    return NotificationServiceConfig(
        kafka=kafka,
        sms=sms
    )