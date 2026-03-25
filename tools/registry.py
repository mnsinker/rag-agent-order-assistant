from tools.base import Tool
from tools.check_refund import check_refund
from tools.get_shipping_status import get_shipping_status


tools = {
    "refund": Tool(
        "check_refund",
        "check whether order is refundable",
        check_refund,
        order_id=str
    ),
    "shipping": Tool(
        "get_shipping_status",
        "check shipping status",
        get_shipping_status,
        order_id=str
    )
}

# print(tools['refund'].args)
# {'order_id': <class 'str'>, 'user_id': <class 'str'>}