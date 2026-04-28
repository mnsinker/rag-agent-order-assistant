from tools.registry import tools
from domain.dtos.refund_dto import RefundEligibilityDTO, RefundExecutionResultDTO

cases = [
    {  # case 1: 订单不存在
        "tool": "get_order",
        "params": {"order_id": "999"},
        "expected": "error"
    },
    { # case 2: 可退款
        "tool": "check_refund",
        "params": {"order_id": "123"},
        "expected": RefundEligibilityDTO(False, "product is already shipped")
    },
    { # case 3: 不可退款 - 已发货
        "tool": "check_refund",
        "params": {"order_id": "789"},
        "expected": RefundEligibilityDTO(False, "custom product doesn't support refund")
    },
    { # case 4: 不可退款 - 定制商品
        "tool": "check_refund",
        "params": {"order_id": "789"},
        "expected": RefundEligibilityDTO(False, "custom product doesn't support refund")
    },
    { # case 5: 可执行退款
        "tool": "create_refund",
        "params": {
            "order_id": "123",
            "eligibility": RefundEligibilityDTO(True, "eligible for refund")
        },
        "expected": RefundExecutionResultDTO(True, 'refund initiated')
    },
    { # case 6: 不可执行退款
        "tool": "create_refund",
        "params": {
            "order_id": "123",
            "eligibility": RefundEligibilityDTO(False, "product is already shipped")
        },
        "expected": RefundExecutionResultDTO(False, 'not eligible to refund')
    }
]

def evaluate(cases: list[dict]):
    results = []
    len_cases = len(cases)
    for case in cases:
        tool = tools.get(case["tool"])
        params = case["params"]
        expected = case["expected"]

        try:
            actual = tool.run(**params)
        except:
            actual = "error"

        correctness = (expected == actual)
        results.append({
            "tool": tool.name,
            "expected": expected,
            "actual": actual,
            "correctness": correctness,
        })
    accuracy = [r["correctness"] for r in results]
    summary = {"Total cases": len_cases, "Accuracy": sum(accuracy) / len_cases}
    return summary, results

if __name__ == "__main__":
    print(evaluate(cases))


'''
{'Total cases': 6, 'Accuracy': 1.0}

[{'tool': 'get_order', 'expected': 'error', 'actual': 'error', 'correctness': True}, 
{'tool': 'check_refund', 'expected': RefundEligibility(refundable=False, reason='product is already shipped'), 'actual': RefundEligibility(refundable=False, reason='product is already shipped'), 'correctness': True}, 
{'tool': 'check_refund', 'expected': RefundEligibility(refundable=False, reason="custom product doesn't support refund"), 'actual': RefundEligibility(refundable=False, reason="custom product doesn't support refund"), 'correctness': True}, 
{'tool': 'check_refund', 'expected': RefundEligibility(refundable=False, reason="custom product doesn't support refund"), 'actual': RefundEligibility(refundable=False, reason="custom product doesn't support refund"), 'correctness': True}, 
{'tool': 'create_refund', 'expected': RefundExecutionResult(success=True, message='refund initiated', refund_id=''), 'actual': RefundExecutionResult(success=True, message='refund initiated', refund_id=''), 'correctness': True}, 
{'tool': 'create_refund', 'expected': RefundExecutionResult(success=False, message='not eligible to refund', refund_id=''), 'actual': RefundExecutionResult(success=False, message='not eligible to refund', refund_id=''), 'correctness': True}]


'''




