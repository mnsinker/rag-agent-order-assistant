from domain.dtos.order_summary_dto import OrderSummaryDTO
from domain.dtos.user_profile_dto import UserProfileDTO
from domain.dtos.user_history_dto import UserHistoryDTO
from services.user_service import get_user_profile, get_user_history_service

def get_user(order: OrderSummaryDTO) -> UserProfileDTO:
    return get_user_profile(order.user_id)


def get_user_history(user: UserProfileDTO) -> UserHistoryDTO:
    return get_user_history_service(user.user_id)