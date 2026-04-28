from llm.responder import generate_final_result
from domain.dtos.refund_dto import RefundEligibilityDTO
from domain.dtos.risk_dto import RiskResultDTO
from domain.dtos.shipping_dto import ShippingResultDTO

# DECISION_SYNONYMS = { # old version
#     "可以退款": ["可以退款", "可退款", "可以申请退款"],
#     "不能退款": ["不能退款", "无法退款", "不支持退款"],
#     "无法判断": ["无法判断", "不确定", "暂无信息", "未找到"]
# }

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
        ("无法提供", 0.8),
        ("无法为您提供", 0.9)
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
        "tool_results": [RefundEligibilityDTO(False, "已发货")],
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
            RefundEligibilityDTO(True, "7天内")
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
        "tool_results": [RefundEligibilityDTO(False, "已发货"), ShippingResultDTO(True, "已送达")],
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
        "tool_results": [RiskResultDTO(False, "没有风险")],
        "expected": {
            "decision": "没有风险",
            "reason": None,   # 这个case 现在不强制reason
            "require_reason": False
        }
    }
]


def get_answers(cases: list) -> list:
    answers = []
    for case in cases:
        query = case["query"]
        tool_results = case["tool_results"]
        answer = generate_final_result(query, tool_results)
        answers.append({
            "case_no": case["case_no"],
            "query": query,
            "tool_results": tool_results,
            "expected": case["expected"],
            "actual_answer": answer
        })
    return answers


def contains_any(text: str, keywords: list) -> bool:
    return any(k in text for k in keywords)

def match_decision(answer: str, expected_decision: str) -> bool:
    synonyms = DECISION_SYNONYMS.get(expected_decision, [expected_decision])
    return any(s in answer for s in synonyms)


def decision_score(answer: str, expected_decision: str) -> float:
    pairs = DECISION_SYNONYMS.get(expected_decision, [(expected_decision, 1.0)])
    total = sum(w for _, w in pairs)
    score = 0

    for k, w in pairs:
        if k in answer:
            score += w

    return score / total if total > 0 else 0  # 避免分母=0报错



def evaluation(cases: list, answers: list):
    results = []
    len_cases = len(cases)
    answer_map = {answer["case_no"]: answer for answer in answers} # 建立映射 ( 避免 2个for → O(n²) )

    for case in cases:
        case_no = case["case_no"]
        expected = case["expected"]
        expected_decision = expected["decision"]
        answer = answer_map[case_no]["actual_answer"]
        error_types = []
        correctness_decision = True
        correctness_reason = True
        correctness_extra = True

        # 1. decision = 可以退款 / 不可退款 (soft score)
        if expected_decision != "无法判断":
            score = decision_score(answer, expected_decision)
            if score < 0.2: # 阈值可调
                correctness_decision = False
                error_types.append("decision_mismatch")
        else: # 无法判断的case
            score = None

        # 2. decision = 无法判断 (safety 隐含在 decision)
        if expected_decision == '无法判断':
            # answer 不允许出现明确结论
            if contains_any(answer,
                            [k for k, _ in DECISION_SYNONYMS["可以退款"]]+
                            [k for k, _ in DECISION_SYNONYMS['不能退款']]
                            ):
                correctness_decision = False
                error_types.append("unsafe_answer")
            # answer 必须表达不确定
            if not contains_any(answer,[k for k, _ in DECISION_SYNONYMS["无法判断"]]):
                correctness_decision = False
                error_types.append("missing_uncertainty")

        # 3. reason
        if expected.get("require_reason"):
            expected_reason = expected.get("reason")
            if expected_reason is None:
                raise ValueError(f'{case_no}: case design problem! require_reason=True, but reason=None')
            reason_pairs = DECISION_SYNONYMS.get(expected_reason, [(expected_reason, 1.0)])
            if not any(k in answer for k, _ in reason_pairs):
                correctness_reason = False
                error_types.append("missing_reason")
            # if expected_reason not in answer:
            #     correctness_reason = False
            #     error_types.append("missing_reason")

        # 4. extra checks (只用于复杂case)
        extra = expected.get('extra_checks', {})
        for k in extra.get("must_include", []):
            if k not in answer:
                correctness_extra = False
                error_types.append("missing_extra_info")

        # 5. 汇总
        final_correctness = (correctness_decision and
                             correctness_reason and
                             correctness_extra)

        results.append({
            "case_no": case_no,
            "answer": answer,
            "decision_score": round(score, 3) if score is not None else None,
            "correctness_decision": correctness_decision,
            "correctness_reason": correctness_reason,
            "correctness_extra": correctness_extra,
            "final_correctness": final_correctness,
            "error_types": error_types
        })

    decision_accuracy = [r.get("correctness_decision") for r in results]

    reason_accuracy = [r.get("correctness_reason") for r,c in zip(results, cases) if c["expected"].get("require_reason")]
    reason_cases = sum(c["expected"].get("require_reason") for c in cases)

    extra_accuracy = [r.get("correctness_extra") for r in results]


    summary = {"Total cases": len_cases,
               "decision_accuracy": round(sum(decision_accuracy)/len_cases, 3),
               "reason_accuracy": sum(reason_accuracy)/reason_cases,
               "extra_accuracy": sum(extra_accuracy)/len_cases}
    return summary, results







if __name__ == '__main__':
    # answers = get_answers(cases)
    answers = [{'case_no': '1.normal grounded answer', 'query': '订单123能退款吗',
               'tool_results': [RefundEligibilityDTO(refundable=False, reason='已发货')],
               'expected': {'decision': '不能退款', 'reason': '已发货', 'require_reason': True},
               'actual_answer': '根据查询结果，订单123目前无法退款，原因是该订单已发货。'},
              {'case_no': '2.positive answer', 'query': '订单123能退款吗',
               'tool_results': [RefundEligibilityDTO(refundable=True, reason='7天内')],
               'expected': {'decision': '可以退款', 'reason': '7天内', 'require_reason': True},
               'actual_answer': '可以退款，订单123符合7天内的退款条件。'},
              {'case_no': '3.multi tool reasoning', 'query': '订单123能退款吗, 顺便看看物流',
               'tool_results': [RefundEligibilityDTO(refundable=False, reason='已发货'),
                                ShippingResultDTO(shipped=True, shipping_status='已送达')],
               'expected': {'decision': '不能退款', 'reason': '已发货', 'require_reason': True,
                            'extra_checks': {'must_include': ['物流', '送达']}},
               'actual_answer': '关于订单123的情况如下：\n\n1.  **退款**：目前无法退款，原因是订单已发货。\n2.  **物流**：订单已发货，并且物流状态为“已送达”。'},
              {'case_no': '4.no result safety', 'query': '订单999能退款吗', 'tool_results': [],
               'expected': {'decision': '无法判断', 'reason': None, 'require_reason': False},
               'actual_answer': '根据查询结果，系统中没有找到订单号为“999”的相关信息，因此无法为您提供该订单的退款状态或进行退款操作。'},
              {'case_no': '5.risk explanation', 'query': '订单123有没有风险',
               'tool_results': [RiskResultDTO(risk=False, reason='没有风险')],
               'expected': {'decision': '没有风险', 'reason': None, 'require_reason': False},
               'actual_answer': '根据系统检测，订单123没有风险。'}]
    summary, results = evaluation(cases, answers)
    print(f'answers: {answers}')
    print(f"summary: {summary} \nresults: {results}")

'''
summary: {'Total cases': 5, 'decision_accuracy': 0.8, 'reason_accuracy': 1.0, 'extra_accuracy': 1.0} 
results: [
{'case_no': '1.normal grounded answer', 
'answer': '根据查询结果，订单123目前无法退款，原因是该订单已发货。', 
'decision_score': 0.222, 
'correctness_decision': True, 'correctness_reason': True, 'correctness_extra': True, 'final_correctness': True, 
'error_types': []}, 

{'case_no': '2.positive answer', 
'answer': '可以退款，订单123符合7天内的退款条件。', 
'decision_score': 0.325, 
'correctness_decision': True, 
'correctness_reason': True, 'correctness_extra': True, 'final_correctness': True, 
'error_types': []}, 

{'case_no': '3.multi tool reasoning', 
'answer': '关于订单123的情况如下：\n\n1.  **退款**：目前无法退款，原因是订单已发货。\n2.  **物流**：订单已发货，并且物流状态为“已送达”。', 
'decision_score': 0.222, 
'correctness_decision': True, 'correctness_reason': True, 'correctness_extra': True, 'final_correctness': True, 
'error_types': []}, 

{'case_no': '4.no result safety', 
'answer': '根据查询结果，系统中没有找到订单号为“999”的相关信息，因此无法为您提供该订单的退款状态或进行退款操作。', 
'decision_score': 0, 
'correctness_decision': False, 'correctness_reason': True, 'correctness_extra': True, 'final_correctness': False, 
'error_types': ['decision_mismatch', 'missing_uncertainty']}, 

{'case_no': '5.risk explanation', 
'answer': '根据系统检测，订单123没有风险。', 
'decision_score': 0.345, 
'correctness_decision': True, 'correctness_reason': True, 'correctness_extra': True, 'final_correctness': True, 
'error_types': []}
]

'''




