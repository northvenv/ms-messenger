import os
import tomllib
import logging
from typing import Any
from pathlib import Path
from datetime import timedelta
from dataclasses import dataclass


from access_service.infrastructure.persistence.config import DBConfig
from access_service.domain.common.entities.config import (
    AccessTokenConfig,
    RefreshTokenConfig,
    VerificationTokenConfig
)
from access_service.infrastructure.web_token.config import JWTConfig
from access_service.presentation.auth.config import TokenAuthConfig
from access_service.infrastructure.cache.config import RedisConfig
from access_service.infrastructure.message_broker.config import KafkaConfig


def load_config_by_path(config_path: Path) -> dict[str, Any]:
    with config_path.open("rb") as cfg:
        return tomllib.load(cfg)


@dataclass
class AccessServiceConfig:
    db: DBConfig
    jwt: JWTConfig
    token_auth: TokenAuthConfig
    access_token: AccessTokenConfig
    verification_token: VerificationTokenConfig
    refresh_token: RefreshTokenConfig
    redis: RedisConfig
    kafka: KafkaConfig


def load_access_service_config() -> AccessServiceConfig:
    db = DBConfig(
        host=os.environ["POSTGRES_HOST"],
        port=int(os.environ["POSTGRES_PORT"]),
        db_name=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

    cfg_path = os.environ["CONFIG_PATH"]
    cfg = load_config_by_path(Path(cfg_path))

    try:
        access_token_key = cfg["auth"]["access-token-key"]
        refresh_token_key = cfg["auth"]["refresh-token-key"]

        jwt_algorithm = cfg["security"]["algorithm"]
        access_token_expires_after = cfg["security"]["access-token-expires-minutes"]
        refresh_token_expires_after = cfg["security"]["refresh-token-expires-days"]

        verification_token_expires_after = cfg["verification"]["verification-token-expires-minutes"]
        verification_token_topic = cfg["verification"]["verification_token_topic"]
        sms_result_topic = cfg["verification"]["sms_result_topic"]

    except KeyError:
        logging.fatal("On startup: Error reading config %s", cfg_path)
        raise

    jwt = JWTConfig(
        key=os.environ["JWT_KEY"],
        algorithm=jwt_algorithm
    )
    
    access_token = AccessTokenConfig(
        expires_after=timedelta(access_token_expires_after),
    )
    refresh_token = RefreshTokenConfig(
        expires_after=timedelta(refresh_token_expires_after),
    )
    verification_token = VerificationTokenConfig(
        expires_after=timedelta(verification_token_expires_after),
    )
    token_auth = TokenAuthConfig(
        access_token_cookie_key=access_token_key,
        refresh_token_cookie_key=refresh_token_key,
    )
    redis = RedisConfig(
        host=os.environ["REDIS_HOST"],
        port=int(os.environ["REDIS_PORT"])
    )
    kafka = KafkaConfig(
        url=os.environ["KAFKA_URL"],
        verification_token_topic=verification_token_topic,
        sms_result_topic=sms_result_topic
    )

    return AccessServiceConfig(
        db=db,
        jwt=jwt,
        access_token=access_token,
        refresh_token=refresh_token,
        verification_token=verification_token,
        token_auth=token_auth,
        redis=redis,
        kafka=kafka,
    )