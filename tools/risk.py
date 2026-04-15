from models.order import OrderSummary
from models.risk import RiskResult
from models.user import UserProfile
from models.user_history import UserHistory


def risk_check(order: OrderSummary, user: UserProfile, history: UserHistory) -> RiskResult:
    if user.level == 'normal' and order.amount > 1000:
        return RiskResult(True, "high amount for normal user")

    if len(history.orders) < 1:
        return RiskResult(True, "new user risk")

    return RiskResult(False, "no risk")