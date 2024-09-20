from pydantic import BaseModel
from datetime import datetime


class ProductSchema(BaseModel):
    title: str
    made_by: str
    created_at: datetime
