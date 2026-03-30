from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    first_name: str
    is_staff: bool
    is_active: bool
    date_joined: Optional[datetime] = None
