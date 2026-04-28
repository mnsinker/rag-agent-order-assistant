from domain.dtos.credit_dto import CreditScoreDTO
from domain.dtos.order_summary_dto import OrderSummaryDTO
from domain.dtos.risk_dto import RiskResultDTO
from domain.dtos.user_profile_dto import UserProfileDTO
from domain.entities.order import Order
from domain.entities.user import  User
from domain.entities.credit import  Credit
from domain.entities.risk import Risk

DTO_TO_ENTITY = {
    OrderSummaryDTO: Order,
    UserProfileDTO: User,
    CreditScoreDTO: Credit,
    RiskResultDTO: Risk,
}