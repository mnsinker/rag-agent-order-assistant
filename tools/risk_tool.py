from domain.dtos.credit_dto import CreditScoreDTO
from domain.dtos.order_summary_dto import OrderSummaryDTO
from domain.dtos.risk_dto import RiskResultDTO
from domain.dtos.user_profile_dto import UserProfileDTO
from tools.user_tool import get_user_history


def risk_check(order: OrderSummaryDTO, user: UserProfileDTO, credit: CreditScoreDTO) -> RiskResultDTO:
    # 从 UserProfile 里, 通过 get_user_history 获取 user history
    history = get_user_history(user)

    if user.level == 'normal' and order.amount > 1000:
        return RiskResultDTO(True, "high amount for normal user")

    if len(history.orders) < 1:
        return RiskResultDTO(True, "new user risk")

    if credit.score < 600:
        return RiskResultDTO(True, "low credit score")

    return RiskResultDTO(False, "no risk")