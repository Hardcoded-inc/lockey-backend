from typing import Optional

def validate(params: dict, fields) -> Optional[dict]:
    for field in fields:
        if(field not in params):
            raise Exception(f"{field} not found in params")

    return params
