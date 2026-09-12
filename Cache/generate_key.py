import hashlib
import json


def create_cache_key(prompt:str, model_name:str, temperature: float=0.0) -> str:
    cache_data = {
        "prompt": prompt,
        "model_name": model_name,
        "temperatue": temperature
    }

    serialize_data = json.dumps(
        cache_data,
        sort_keys=True,
    )

    return hashlib.sha256(
        serialize_data.encode("utf-8") 
    ).hexdigest()