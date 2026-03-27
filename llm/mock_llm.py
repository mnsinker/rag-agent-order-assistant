from models.refund import RefundEligibility
def mock_llm(query: str, schemas: list) -> dict:
    return {
        "steps": [
            {"tool": "check_refund", "args": {"order_id": "123"}},
            {"tool": "create_refund", "args": {"order_id": "123", 'eligibility': RefundEligibility}}
        ]
    }
