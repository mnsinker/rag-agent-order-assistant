from models.refund import RefundEligibility
from models.risk import RiskResult
from models.shipping import ShippingResult

DECISION_SYNONYMS = {
    "可以退款": [
        ("可以退款", 1.0),
        ("可退款", 1.0),
        ("可以申请退款", 0.9),
        ("符合退款条件", 0.8),
        ("可以", 0.3),
    ],
    "不能退款": [
        ("不能退款", 1.0),
        ("无法退款", 1.0),
        ("不支持退款", 0.9),
        ("不能处理退款", 0.8),
        ("无法处理退款", 0.8),
    ],
    "无法判断": [
        ("无法判断", 1.0),
        ("不确定", 1.0),
        ("暂无信息", 0.9),
        ("未找到", 0.9),
        ("未能找到", 0.9),
        ("无法查询", 0.8),
        ("无法处理", 0.7),
    ],
    "没有风险": [
        ("没有风险", 1.0),
        ("无风险", 1.0),
        ("未发现风险", 0.9),
    ]
}

cases = [
    { # case 1. 正常回答
        "case_no": "1.normal grounded answer",
        "query": "订单123能退款吗",
        "tool_results": [RefundEligibility(False, "已发货")],
        "expected": {
            "decision": "不能退款",
            "reason": "已发货",
            "require_reason": True
        }
    },
    { # case 2. 可退款
        "case_no": "2.positive answer",
        "query": "订单123能退款吗",
        "tool_results": [
            RefundEligibility(True, "7天内")
        ],
        "expected": {
            "decision": "可以退款",
            "reason": "7天内",
            "require_reason": True
        }
    },
    { # case 3. 多工具结果（组合）
        "case_no": "3.multi tool reasoning",
        "query": "订单123能退款吗, 顺便看看物流",
        "tool_results": [RefundEligibility(False, "已发货"), ShippingResult(True, "已送达")],
        "expected": {
            "decision": "不能退款",
            "reason": "已发货",
            "require_reason": True,
            "extra_checks": {
                "must_include": ["物流", "送达"]
            }
        }
    },
    { # case 4. 无结果（安全）
        "case_no": "4.no result safety",
        "query": "订单999能退款吗",
        "tool_results": [],
        "expected": {
            "decision": "无法判断",
            "reason": None,
            "require_reason": False
        }
    },
    { # case 5. 风险判断
        "case_no": "5.risk explanation",
        "query": "订单123有没有风险",
        "tool_results": [RiskResult(False, "没有风险")],
        "expected": {
            "decision": "没有风险",
            "reason": None,   # 这个case 现在不强制reason
            "require_reason": False
        }
    }
]
