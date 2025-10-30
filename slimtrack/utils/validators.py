def validate_weight(weight_str: str) -> tuple[bool, float]:
    try:
        weight = float(weight_str)
        if weight <= 0 or weight > 300:
            return False, 0
        return True, weight
    except ValueError:
        return False, 0

def validate_height(height_str: str) -> tuple[bool, float]:
    try:
        height = float(height_str)
        if height <= 0 or height > 3:
            return False, 0
        return True, height
    except ValueError:
        return False, 0