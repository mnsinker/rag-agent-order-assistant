from models.risk import RiskResult
from models.user import UserProfile
from models.user_history import UserHistory
from services.user_service import get_user_profile, get_user_history_service

def get_user(user_id: str) -> UserProfile:
    return get_user_profile(user_id)


def get_user_history(user_id: str) -> UserHistory:
    return get_user_history_service(user_id)