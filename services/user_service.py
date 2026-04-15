from errors.validation import ValidationError
from models.user import UserProfile
from models.user_history import UserHistory, OrderRecord


def get_user_profile(user_id: str) -> UserProfile:
        users = {
            "u1": {"level": "vip"},
            "u2": {"level": "normal"}
        }

        user = users.get(user_id)
        if not user:
            return UserProfile(user_id, "normal")
        return UserProfile(user_id, user["level"])


def get_user_history_service(user_id: str) -> UserHistory:
    fake_db = {
        "u1": [
                {"order_id": "o1", "amount": 100},
                {"order_id": "o2", "amount": 200},
            ],
        "u2": [],
    }
    rows = fake_db.get(user_id)

    if rows is None:
        raise ValidationError(f'user {user_id} not found')
    return UserHistory(
        user_id=user_id,
        orders=[OrderRecord(order_id=r['order_id'], amount=r['amount']) for r in rows]
    )
