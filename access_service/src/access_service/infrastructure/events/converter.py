import orjson
from dataclasses import asdict
from access_service.domain.common.events.base import BaseEvent
from uuid import UUID
from typing import Any


def convert_event_to_broker_message(event: BaseEvent) -> bytes:
    def convert(obj: Any) -> Any:
        if isinstance(obj, UUID): 
            return str(obj)  
        elif isinstance(obj, dict):  
            return {k: convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):  
            return [convert(v) for v in obj]
        return obj  
    event_dict = {k: convert(v) for k, v in event.__dict__.items()}
    return orjson.dumps(event_dict)


def convert_event_to_json(event: BaseEvent) -> dict[str, any]:
    return asdict(event)

