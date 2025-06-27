# schemas.py
from pydantic import BaseModel
from typing import Any, Dict

class ProcessImageRequest(BaseModel):
    algorithm: str
    parameters: Dict[str, Any]
    image: str
