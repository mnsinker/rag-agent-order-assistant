from models.credit import CreditScore


def get_user_credit(user_id: str) -> CreditScore:
    return CreditScore(score=700)