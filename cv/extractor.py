import re

def extract_total(raw_text: str) -> float | None:
    if not raw_text:
        return None

    cleaned_lines = [line.strip() for line in raw_text.upper().splitlines() if line.strip()]
    full_cleaned_text = "\n".join(cleaned_lines)
    price_regex = r"\d+(?:[.,]\d+)*\.\d{2}"

    keywords = ["GRAND TOTAL","CASH", "AMOUNT DUE", "NET AMOUNT", "TOTAL"]
    for keyword in keywords:
        for line in cleaned_lines:
            if keyword in line:
                possible_amounts = re.findall(price_regex, line)
                
                for amount_str in possible_amounts:
                    sanitized_amount = amount_str.replace(",", "")
                    val = float(sanitized_amount)
                    
                    match_idx = line.find(amount_str)
                    start_look = max(0, match_idx - 5)
                    end_look = min(len(line), match_idx + len(amount_str) + 5)
                    surrounding_context = line[start_look:end_look]
                    
                    if "%" not in surrounding_context:
                        return val
                    
    all_amounts = re.findall(price_regex, full_cleaned_text)
    valid_fallback_values = []
    
    for amount_str in all_amounts:
        sanitized_amount = amount_str.replace(",", "")
        try:
            val = float(sanitized_amount)
            if val >= 5.00:
                valid_fallback_values.append(val)
        except ValueError:
            continue

    if valid_fallback_values:
        return max(valid_fallback_values)

    return None