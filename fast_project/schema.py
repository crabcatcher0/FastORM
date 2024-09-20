from pydantic import BaseModel
from datetime import datetime


class GenericSchema(BaseModel):
    detail: str
