import json
from datetime import datetime
from dataclasses import is_dataclass, asdict
from typing import Any


def custom_encoder(o):
    if isinstance(o, datetime):
        return o.isoformat()  
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


def convert_string_to_dict(string: str) -> dict:
    data_dict = json.loads(string)
    return data_dict
    

def convert_dataclass_to_json(data: Any):
    data_dict = asdict(data)
    return json.dumps(
        data_dict, 
        default=custom_encoder, 
        ensure_ascii=False,
        indent=4
    )

