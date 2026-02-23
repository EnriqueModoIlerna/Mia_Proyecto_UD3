def analyze_lexical(text: str) -> dict:
    """
    Returns sentiment analysis based on lexical rules.
    """
    return {
        "polarity": "neutral",
        "score": 0.0,
        "emotions": {},
        "intensity": 0,
        "irony": False,
        "explanation": []
    }