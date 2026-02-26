"""
transformer_analyzer.py
Analizador basado en modelos preentrenados (Transformers)
"""

from transformers import pipeline

# ======================================================
# CONFIGURACIÓN MODELOS
# ======================================================

SENTIMENT_MODEL = "pysentimiento/robertuito-sentiment-analysis"
EMOTION_MODEL = "pysentimiento/robertuito-emotion-analysis"

_sentiment_pipeline = None
_emotion_pipeline = None


# ======================================================
# CARGA DIFERIDA (lazy loading)
# ======================================================

def load_models():
    global _sentiment_pipeline, _emotion_pipeline

    if _sentiment_pipeline is None:
        _sentiment_pipeline = pipeline(
            "text-classification",
            model=SENTIMENT_MODEL,
            tokenizer=SENTIMENT_MODEL
        )

    if _emotion_pipeline is None:
        _emotion_pipeline = pipeline(
            "text-classification",
            model=EMOTION_MODEL,
            tokenizer=EMOTION_MODEL,
            top_k=None
        )


# ======================================================
# NORMALIZADORES
# ======================================================

def normalize_label(label):
    label = label.lower()

    if "pos" in label:
        return "positive"
    if "neg" in label:
        return "negative"
    if "neu" in label:
        return "neutral"

    return label


# ======================================================
# ANÁLISIS PRINCIPAL
# ======================================================

def analyze_model(text):
    """
    Analiza texto usando modelos Transformer

    Returns
    -------
    dict
    """

    load_models()

    explanations = []

    # --------------------------------------------------
    # SENTIMIENTO
    # --------------------------------------------------

    sentiment_result = _sentiment_pipeline(text)[0]

    polarity = normalize_label(sentiment_result["label"])
    score = sentiment_result["score"]

    explanations.append(
        f"Modelo predice sentimiento '{polarity}' con confianza {score:.2f}"
    )

    # --------------------------------------------------
    # EMOCIONES
    # --------------------------------------------------

    emotions_raw = _emotion_pipeline(text)[0]

    emotions = {}

    for e in emotions_raw:
        emotions[e["label"]] = round(e["score"], 3)

    explanations.append("Emociones detectadas por modelo")

    # --------------------------------------------------
    # INTENSIDAD
    # --------------------------------------------------

    intensity = max(emotions.values()) if emotions else score

    # --------------------------------------------------
    # OUTPUT FINAL
    # --------------------------------------------------

    return {
        "source": "transformer_model",
        "polarity": polarity,
        "score": round(score, 3),
        "intensity": round(float(intensity), 3),
        "emotions": emotions,
        "explanation": explanations
    }