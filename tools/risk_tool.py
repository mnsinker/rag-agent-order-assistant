from domain.dtos.credit_dto import CreditScoreDTO
from domain.dtos.order_summary_dto import OrderSummaryDTO
from domain.dtos.risk_dto import RiskResultDTO
from domain.dtos.user_profile_dto import UserProfileDTO
from tests.policies.test_risk_policy import evaluate_risk_policy


def risk_check(
        order: OrderSummaryDTO,
        user: UserProfileDTO,
        credit: CreditScoreDTO
) -> RiskResultDTO:
    return evaluate_risk_policy(order, user, credit)