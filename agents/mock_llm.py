def mock_llm(query: str, schemas: list):
    return {
                "tool": "check_refund",
                "args": {
                    "order_id": "123"
                }
            }