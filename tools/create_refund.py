from models.refund import RefundExecutionResult
from models.refund import RefundEligibility
from errors.tool import ToolError
def create_refund(order_id: str, eligibility: RefundEligibility | None = None) -> RefundExecutionResult:
    if eligibility and not eligibility.refundable:
        return RefundExecutionResult(False, 'not eligible to refund')
    return RefundExecutionResult(True, 'refund initiated')
