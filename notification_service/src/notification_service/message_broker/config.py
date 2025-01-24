from dataclasses import dataclass


@dataclass 
class BaseBrokerConfig:
    url: str


@dataclass
class KafkaConfig(BaseBrokerConfig): 
    verification_token_topic: str
    sms_result_topic: str