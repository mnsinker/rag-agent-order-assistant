import re

def extract_order_id(query: str) -> str | None:
    matches = re.findall(r'\d+', query)
    return matches[0] if matches else None


extractors = {
    'order_id': extract_order_id
}


