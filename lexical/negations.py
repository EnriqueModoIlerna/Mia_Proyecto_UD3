"""
negations.py
Detección de negaciones y su ámbito usando spaCy
"""


# ======================================================
# LISTA DE NEGACIONES
# ======================================================

NEGATION_WORDS = [
    "no",
    "nunca",
    "jamás",
    "ni",
    "tampoco",
    "nadie",
    "nada"
]


# ======================================================
# DETECCIÓN DE NEGACIONES CON DEPENDENCIAS
# ======================================================

def detect_negations(doc):
    """
    Detecta negaciones y determina si afectan
    a palabras con carga sentimental.

    Returns
    -------
    dict
    {
        "negated": bool,
        "negation_words": list,
        "scope_tokens": list,
        "explanation": list
    }
    """

    negation_words_found = []
    scope_tokens = []
    explanations = []

    for token in doc:

        # Caso 1: palabra explícita de negación
        if token.text.lower() in NEGATION_WORDS:
            negation_words_found.append(token.text.lower())

            # Intentamos encontrar qué palabra afecta
            # Generalmente será el head del token
            head = token.head

            if head:
                scope_tokens.append(head.text)
                explanations.append(
                    f"Negación '{token.text}' afecta a '{head.text}'"
                )

        # Caso 2: dependencia gramatical "neg"
        if token.dep_ == "neg":
            negation_words_found.append(token.text.lower())

            head = token.head
            if head:
                scope_tokens.append(head.text)
                explanations.append(
                    f"Dependencia negativa detectada en '{head.text}'"
                )

    negated = len(negation_words_found) > 0

    return {
        "negated": negated,
        "negation_words": list(set(negation_words_found)),
        "scope_tokens": list(set(scope_tokens)),
        "explanation": explanations
    }