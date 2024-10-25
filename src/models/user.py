from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    user_name: str
    password: str
    group: str
    id: Optional[int] = None
    login_attempts: int = 0
    locked_until: Optional[datetime] = None

