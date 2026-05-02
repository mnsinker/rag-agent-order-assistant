import re
import json

def safe_parse_llm_output(content: str) -> dict | None:
    try:
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if not match:
            return None
        return json.loads(match.group())

    except Exception as e:
        print(f'[PARSE ERROR]] {e}')
        return None
