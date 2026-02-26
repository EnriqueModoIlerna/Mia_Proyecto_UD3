"""
irony_rules.py
Detección de ironía basada en reglas simples
"""


# ======================================================
# PATRONES DE IRONÍA
# ======================================================

IRONY_PHRASES = [
    "sí claro",
    "si claro",
    "claro claro",
    "perfecto...",
    "genial...",
    "qué maravilla",
    "maravilloso...",
    "fantástico...",
    "increíble..."
]

IRONY_EMOJIS = [
    "🙄", "😒", "😑", "😏", "🤨", "😬"
]

POSITIVE_WORDS = [
    "excelente", "perfecto", "maravilloso",
    "fantástico", "genial", "increíble"
]

NEGATIVE_CONTEXT = [
    "tarde", "mal", "error", "problema",
    "horrible", "fatal", "lento", "caro"
]


# ======================================================
# REGLAS DE DETECCIÓN
# ======================================================

def contains_ironic_phrase(text):
    text_low = text.lower()
    for phrase in IRONY_PHRASES:
        if phrase in text_low:
            return True, f"Frase irónica detectada: '{phrase}'"
    return False, None


def contains_ironic_quotes(text):
    if '"' in text or "'" in text:
        for word in POSITIVE_WORDS:
            if f'"{word}"' in text.lower() or f"'{word}'" in text.lower():
                return True, f"Palabra positiva entre comillas: {word}"
    return False, None


def contains_ironic_emoji(text):
    for emoji in IRONY_EMOJIS:
        if emoji in text:
            return True, f"Emoji irónico detectado: {emoji}"
    return False, None


def contradiction_rule(text):
    text_low = text.lower()

    pos_found = any(p in text_low for p in POSITIVE_WORDS)
    neg_found = any(n in text_low for n in NEGATIVE_CONTEXT)

    if pos_found and neg_found:
        return True, "Contradicción positiva + contexto negativo"

    return False, None


# ======================================================
# FUNCIÓN PRINCIPAL
# ======================================================

def detect_irony(text):
    """
    Detecta ironía básica en texto

    Returns
    -------
    dict
    {
        irony: bool,
        score: float,
        explanation: list
    }
    """

    explanations = []
    score = 0

    # regla 1 — frases típicas
    result, exp = contains_ironic_phrase(text)
    if result:
        score += 0.4
        explanations.append(exp)

    # regla 2 — comillas irónicas
    result, exp = contains_ironic_quotes(text)
    if result:
        score += 0.3
        explanations.append(exp)

    # regla 3 — emojis
    result, exp = contains_ironic_emoji(text)
    if result:
        score += 0.3
        explanations.append(exp)

    # regla 4 — contradicción semántica
    result, exp = contradiction_rule(text)
    if result:
        score += 0.5
        explanations.append(exp)

    # límite máximo
    score = min(score, 1.0)

    return {
        "irony": score > 0.4,
        "score": round(score, 3),
        "explanation": explanations
    }