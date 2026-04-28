from domain.dtos.credit_dto import CreditScoreDTO
from domain.dtos.user_profile_dto import UserProfileDTO


def get_user_credit(user: UserProfileDTO) -> CreditScoreDTO:
    if user.level == "vip":
        return CreditScoreDTO(score=800)
    return CreditScoreDTO(score=200)