from dataclasses import dataclass


@dataclass 
class BaseBrokerConfig:
    url: str
    verification_token_topic: str
    sms_result_topic: str

@dataclass
class KafkaConfig(BaseBrokerConfig): ...