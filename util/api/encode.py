from json import dumps
from fastapi import Response

def encode_json(data: dict) -> Response:
    return Response(content=dumps(data), media_type="application/json")
