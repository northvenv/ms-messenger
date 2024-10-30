from dataclasses import dataclass


@dataclass 
class BaseKafkaConfig:
    kafka_url: str

    # def get_connection_url(self) -> str:
    #     return f"kafka:{self.port}"

@dataclass
class KafkaConfig(BaseKafkaConfig): ...