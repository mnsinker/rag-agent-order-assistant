from domain.dtos.credit_dto import CreditScoreDTO
from domain.dtos.order_summary_dto import OrderSummaryDTO
from domain.dtos.user_profile_dto import UserProfileDTO
from policies.risk_policy import evaluate_risk_policy



def make_order(amount=100):
    return OrderSummaryDTO(
        order_id="test999",
        user_id="test_u1",
        days=3,
        shipped=False,
        custom=False,
        amount=amount,
    )

def test_risk_high_low_credit():
    result = evaluate_risk_policy(
        order=make_order(amount=100),
        user=UserProfileDTO(user_id="test_u1", level="vip"),
        credit=CreditScoreDTO(score=500),
    )
    assert result.risk is True
    assert result.risk_level == "high"
    assert result.policy_rule == "risk.block.low_credit_score"

def test_risk_medium_high_amount_non_vip():
    result = evaluate_risk_policy(
        order=make_order(amount=1500),
        user=UserProfileDTO(user_id="test_u1", level="normal"),
        credit=CreditScoreDTO(score=700),
    )
    assert result.risk is True
    assert result.risk_level == "medium"
    assert result.policy_rule == "risk.block.high_amount_non_vip"

def test_risk_low_vip_good_credit():
    result = evaluate_risk_policy(
        order=make_order(amount=1500),
        user=UserProfileDTO(user_id="test_u1", level="vip"),
        credit=CreditScoreDTO(score=750),
    )
    assert result.risk is False
    assert result.risk_level == "low"
    assert result.policy_rule == "risk.allow.vip_good_credit"

