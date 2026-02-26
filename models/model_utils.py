"""
model_utils.py
Funciones auxiliares para normalizar resultados de modelos
"""


# ======================================================
# NORMALIZAR ETIQUETAS
# ======================================================

def normalize_sentiment_label(label):
    """
    Convierte etiquetas del modelo en:
    positive / negative / neutral
    """

    label = label.lower()

    if "pos" in label:
        return "positive"
    if "neg" in label:
        return "negative"
    if "neu" in label:
        return "neutral"

    return label


# ======================================================
# CONVERTIR SCORE A POLARIDAD
# ======================================================

def score_to_polarity(score, threshold=0.5):
    """
    Convierte score continuo en etiqueta
    """

    if score > threshold:
        return "positive"
    elif score < (1 - threshold):
        return "negative"
    else:
        return "neutral"


# ======================================================
# NORMALIZAR EMOCIONES
# ======================================================

def normalize_emotions(emotions_list):
    """
    Convierte salida raw del modelo en dict limpio
    """

    emotions = {}

    for e in emotions_list:
        emotions[e["label"]] = round(float(e["score"]), 3)

    return emotions


# ======================================================
# INTENSIDAD DESDE EMOCIONES
# ======================================================

def get_intensity_from_emotions(emotions_dict):
    """
    Intensidad = emoción dominante
    """

    if not emotions_dict:
        return 0.0

    return max(emotions_dict.values())