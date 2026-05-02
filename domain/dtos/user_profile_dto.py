from dataclasses import dataclass
from typing import ClassVar, Type
from domain.entities.base import Entity
from domain.entities.user import User


@dataclass
class UserProfileDTO: # Model
    user_id: str
    level: str  # normal / vip ...
    entity: ClassVar[Type[Entity]] = User

