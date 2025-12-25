def generate_explanation(result):
    reasons = []

    if result["status"] == "REJECTED":
        if "LEXICAL" in result["policy_code"]:
            reasons.append("Title is phonetically or lexically similar to an existing registered title.")
        if "SEMANTIC" in result["policy_code"]:
            reasons.append("Title conveys the same meaning as an existing registered title.")
    
    if result["status"] == "MANUAL_REVIEW":
        reasons.append("Title shows partial similarity and requires human verification.")

    if not reasons:
        reasons.append("No conflicts found under PRGI guidelines.")

    return reasons
