from errors.validation import ValidationError
from domain.dtos.user_profile_dto import UserProfileDTO
from domain.dtos.user_history_dto import UserHistoryDTO, OrderRecordDTO


def get_user_profile(user_id: str) -> UserProfileDTO:
        users = {
            "u1": {"level": "vip"},
            "u2": {"level": "normal"}
        }

        user = users.get(user_id)
        if not user:
            return UserProfileDTO(user_id, "normal")
        return UserProfileDTO(user_id, user["level"])


def get_user_history_service(user_id: str) -> UserHistoryDTO:
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
    return UserHistoryDTO(
        user_id=user_id,
        orders=[OrderRecordDTO(order_id=r['order_id'], amount=r['amount']) for r in rows]
    )
