from models.credit import CreditScore
from models.order import OrderSummary
from models.risk import RiskResult
from models.user import UserProfile
from models.user_history import UserHistory


def risk_check(order: OrderSummary, user: UserProfile, history: UserHistory, credit: CreditScore) -> RiskResult:
    if user.level == 'normal' and order.amount > 1000:
        return RiskResult(True, "high amount for normal user")

    if len(history.orders) < 1:
        return RiskResult(True, "new user risk")

    if credit.score < 600:
        return RiskResult(True, "low credit score")

    return RiskResult(False, "no risk")