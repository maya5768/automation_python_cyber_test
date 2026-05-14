import re


def parse_price(text: str) -> float:
    """
    "$110.00 Ex Tax: $100.00"  ->  110.0
    "$1,299.00"                ->  1299.0
    """
    match = re.search(r'\$?([\d,]+\.?\d*)', text.split('\n')[0])
    if match:
        return float(match.group(1).replace(',', ''))
    return 0.0
