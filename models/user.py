from dataclasses import dataclass

@dataclass
class UserProfile: # Model
    user_id: str
    level: str  # normal / vip

