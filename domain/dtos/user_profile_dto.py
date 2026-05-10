from dataclasses import dataclass
from typing import ClassVar, Type

from domain.nodes.base import Node
from domain.nodes.user import UserProfile


@dataclass
class UserProfileDTO: # Model
    user_id: str
    level: str  # normal / vip ...
    node: ClassVar[Type[Node]] = UserProfile

