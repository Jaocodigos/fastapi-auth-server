from typing import List

from pydantic import BaseModel

class UserStoreCreate(BaseModel):
    name: str
    type: str
    clients: List[str]


class UserStoreResponse(BaseModel):
    id: str
    name: str
    type: str
