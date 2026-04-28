from dataclasses import dataclass

@dataclass
class UserProfileDTO: # Model
    user_id: str
    level: str  # normal / vip

