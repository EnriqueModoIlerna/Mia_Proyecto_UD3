"""
lexical_analyzer.py
Analizador léxico basado en reglas lingüísticas
"""

import spacy

from lexical.intensifiers import apply_intensity
from lexical.negations import detect_negations
from lexical.irony_rules import detect_irony


# ======================================================
# CARGA MODELO SPACY
# ======================================================

try:
    nlp = spacy.load("es_core_news_sm")
except:
    raise OSError(
        "No tienes instalado el modelo de spaCy.\n"
        "Ejecuta:\n"
        "python -m spacy download es_core_news_sm"
    )


# ======================================================
# LEXICÓN BÁSICO
# ======================================================

POSITIVE_WORDS = {
    "bueno": 0.6,
    "genial": 0.9,
    "excelente": 1.0,
    "perfecto": 1.0,
    "feliz": 0.8,
    "maravilloso": 1.0,
    "increíble": 0.9,
    "encantar": 1.0,
    "gustar": 0.6
}

NEGATIVE_WORDS = {
    "malo": -0.6,
    "horrible": -1.0,
    "terrible": -1.0,
    "fatal": -0.9,
    "odio": -1.0,
    "lento": -0.5,
    "caro": -0.4,
    "error": -0.7,
    "problema": -0.6
}


# ======================================================
# DETECTAR PALABRAS DE SENTIMIENTO
# ======================================================

def detect_sentiment_words(doc):

    words = []
    score = 0

    for token in doc:
        lemma = token.lemma_.lower()

        if lemma in POSITIVE_WORDS:
            val = POSITIVE_WORDS[lemma]
            score += val
            words.append((lemma, val))

        elif lemma in NEGATIVE_WORDS:
            val = NEGATIVE_WORDS[lemma]
            score += val
            words.append((lemma, val))

    return score, words


# ======================================================
# POLARIDAD FINAL
# ======================================================

def label_from_score(score):

    if score > 0.2:
        return "positive"
    elif score < -0.2:
        return "negative"
    elif -0.2 <= score <= 0.2 and abs(score) > 0.05:
        return "mixed"
    else:
        return "neutral"


# ======================================================
# FUNCIÓN PRINCIPAL
# ======================================================

def analyze_lexical(text):
    """
    Analiza texto usando reglas lingüísticas

    Returns
    -------
    dict
    """

    doc = nlp(text)

    explanations = []

    # --------------------------------------------------
    # 1 Detectar palabras sentimentales
    # --------------------------------------------------

    base_score, words = detect_sentiment_words(doc)

    if words:
        explanations.append(
            f"Palabras detectadas: {', '.join([w[0] for w in words])}"
        )

    # --------------------------------------------------
    # 2 Negaciones
    # --------------------------------------------------

    neg_info = detect_negations(doc)

    if neg_info["negated"]:
        base_score *= -1
        explanations.append("Negación detectada → polaridad invertida")

    # --------------------------------------------------
    # 3 Intensidad
    # --------------------------------------------------

    intensity_info = apply_intensity(doc, base_score)

    final_score = intensity_info["score"]

    explanations.extend(intensity_info["explanation"])

    # --------------------------------------------------
    # 4 Ironía
    # --------------------------------------------------

    irony = detect_irony(text)

    if irony["irony"]:
        explanations.append("Posible ironía detectada")
        explanations.extend(irony["explanation"])

    # --------------------------------------------------
    # 5 Polaridad final
    # --------------------------------------------------

    polarity = label_from_score(final_score)

    # intensidad normalizada
    intensity = min(abs(final_score), 1.0)

    # --------------------------------------------------
    # OUTPUT FINAL
    # --------------------------------------------------

    return {
        "source": "lexical_rules",
        "polarity": polarity,
        "score": round(final_score, 3),
        "intensity": round(intensity, 3),
        "irony": irony["irony"],
        "explanation": explanations
    }