from datetime import datetime
from schemas.base import BaseComplaint

from models.enums import State


class ComplaintOut(BaseComplaint):
    id: int
    photo_url: str
    created_at: datetime
    status: State

