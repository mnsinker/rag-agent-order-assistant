from datetime import datetime

"""
Audit Log Schema (contract)
{
  "step": str,
  "tool": str | None,
  "input": dict | None,
  "output": dict | None,
  "error": str | None
}
"""

class AuditLogger:
    STEPS_ALLOWED = {
        "llm_raw",
        "before_tool",
        "after_tool",
        "final_answer",
        "error"
    }

    def __init__(self):
        self.logs = []

    def log(self, step: str, **kwargs):
        if step not in self.STEPS_ALLOWED:
            print(f'[AUDIT WARNING] invalid step: {step}')
            return

        self.logs.append({"step": step, **kwargs})

    def get_logs(self):
        return self.logs

