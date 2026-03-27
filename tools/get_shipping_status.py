from services.order_service import get_order_summary
from models.shipping import ShippingResult
from errors.validation import ValidationError
def get_shipping_status(order_id: str):
    # 1. 获取订单数据
    order_summary = get_order_summary(order_id) # 这里返回是 OrderSummary 对象

    # 2. 检查是否成功
    if order_summary is None:
        raise ValidationError("order_id not found")

    # 3. 从响应中提取数据
    shipped = order_summary.shipped
    shipping_status = "已发货" if shipped else "未发货"
    return ShippingResult(shipped, shipping_status)


'''
    # 2. 检查是否成功
    if order_summary is None:
        return make_response(False, None, "order_id not found")
'''
