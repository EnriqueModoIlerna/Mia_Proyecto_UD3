"""
intensifiers.py
Gestión de intensificadores y atenuadores de sentimiento
"""

# ======================================================
# LISTAS DE MODIFICADORES
# ======================================================

INTENSIFIERS = {
    "muy": 1.5,
    "mucho": 1.4,
    "muchísimo": 2.0,
    "super": 1.8,
    "súper": 1.8,
    "extremadamente": 2.0,
    "demasiado": 1.7,
    "realmente": 1.3,
    "totalmente": 1.6,
    "absolutamente": 1.7
}

DIMINISHERS = {
    "algo": 0.7,
    "un poco": 0.6,
    "poco": 0.75,
    "apenas": 0.5,
    "ligeramente": 0.6,
    "medianamente": 0.8,
    "relativamente": 0.85
}


# ======================================================
# DETECCIÓN DE MODIFICADORES
# ======================================================

def detect_intensifiers(doc):
    """
    Detecta modificadores dentro de un Doc de spaCy

    Returns
    -------
    list
        lista de modificadores encontrados
    """

    found = []

    for token in doc:
        word = token.text.lower()

        if word in INTENSIFIERS:
            found.append({
                "word": word,
                "type": "intensifier",
                "value": INTENSIFIERS[word]
            })

        elif word in DIMINISHERS:
            found.append({
                "word": word,
                "type": "diminisher",
                "value": DIMINISHERS[word]
            })

    return found


# ======================================================
# CÁLCULO DE FACTOR TOTAL
# ======================================================

def calculate_intensity_multiplier(modifiers):
    """
    Calcula multiplicador total según modificadores encontrados
    """

    multiplier = 1.0

    for mod in modifiers:
        multiplier *= mod["value"]

    return multiplier


# ======================================================
# EXPLICACIÓN HUMANA
# ======================================================

def explain_modifiers(modifiers):
    """
    Genera texto explicativo de modificadores detectados
    """

    explanations = []

    for mod in modifiers:
        if mod["type"] == "intensifier":
            explanations.append(f"Intensificador detectado: '{mod['word']}'")
        else:
            explanations.append(f"Atenuador detectado: '{mod['word']}'")

    return explanations


# ======================================================
# FUNCIÓN PRINCIPAL
# ======================================================

def apply_intensity(doc, base_score):
    """
    Ajusta score según intensificadores

    Returns
    -------
    dict
    {
        score,
        multiplier,
        modifiers,
        explanation
    }
    """

    modifiers = detect_intensifiers(doc)
    multiplier = calculate_intensity_multiplier(modifiers)

    final_score = base_score * multiplier

    return {
        "score": final_score,
        "multiplier": multiplier,
        "modifiers": modifiers,
        "explanation": explain_modifiers(modifiers)
    }