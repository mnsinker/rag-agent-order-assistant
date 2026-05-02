from domain.dtos.credit_dto import CreditScoreDTO
from domain.dtos.order_summary_dto import OrderSummaryDTO
from domain.dtos.risk_dto import RiskResultDTO
from domain.dtos.user_profile_dto import UserProfileDTO


def evaluate_risk_policy(
        order: OrderSummaryDTO,
        user: UserProfileDTO,
        credit: CreditScoreDTO,
) -> RiskResultDTO:
   if credit.score < 600:
       return RiskResultDTO(risk=True, risk_level="high", risk_score=90, reason="low credit score", policy_rule="risk.block.low_credit_score")
   if order.amount > 1000 and user.level != "vip":
       return RiskResultDTO(risk=True, risk_level="medium", risk_score=70, reason="high amount order from non-vip user", policy_rule="risk.block.high_amount_non_vip")
   if credit.score >= 700 and user.level == "vip" :
       return RiskResultDTO(risk=False, risk_level="low", risk_score=10, reason="vip user with good credit score", policy_rule="risk.allow.vip_good_credit")
   return RiskResultDTO(risk=False, risk_level="low", risk_score=20, reason="no risk", policy_rule="risk.allow.standard")