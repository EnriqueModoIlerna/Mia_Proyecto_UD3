"""
fusion_engine.py
Fusión del analizador léxico + modelo Transformer
"""


# ======================================================
# PESOS DEL ENSEMBLE
# ======================================================

LEXICAL_WEIGHT = 0.4
MODEL_WEIGHT = 0.6


# ======================================================
# CONVERTIR POLARIDAD A SCORE NUMÉRICO
# ======================================================

def polarity_to_numeric(label):

    mapping = {
        "positive": 1,
        "negative": -1,
        "neutral": 0,
        "mixed": 0
    }

    return mapping.get(label, 0)


# ======================================================
# DECIDIR POLARIDAD FINAL
# ======================================================

def numeric_to_label(score):

    if score > 0.2:
        return "positive"
    elif score < -0.2:
        return "negative"
    elif -0.2 <= score <= 0.2 and abs(score) > 0.05:
        return "mixed"
    else:
        return "neutral"


# ======================================================
# FUNCIÓN PRINCIPAL DE FUSIÓN
# ======================================================

def fusion_results(lexical, model):
    """
    Combina ambos análisis
    """

    explanations = []

    # --------------------------------------------------
    # Caso sin modelo
    # --------------------------------------------------

    if model is None:
        explanations.append("Solo análisis léxico disponible")
        explanations.extend(lexical.get("explanation", []))

        return lexical

    # --------------------------------------------------
    # Convertir polaridades a números
    # --------------------------------------------------

    lex_score = lexical.get("score", 0)
    model_score = polarity_to_numeric(model.get("polarity", "neutral")) * model.get("score", 0)

    explanations.append(
        f"Score léxico: {lex_score}"
    )

    explanations.append(
        f"Score modelo: {model_score}"
    )

    # --------------------------------------------------
    # FUSIÓN PONDERADA
    # --------------------------------------------------

    final_score = (
        lex_score * LEXICAL_WEIGHT +
        model_score * MODEL_WEIGHT
    )

    explanations.append(
        f"Fusión ponderada ({LEXICAL_WEIGHT}/{MODEL_WEIGHT}) aplicada"
    )

    # --------------------------------------------------
    # Polaridad final
    # --------------------------------------------------

    final_polarity = numeric_to_label(final_score)

    # --------------------------------------------------
    # Intensidad
    # --------------------------------------------------

    intensity = max(
        abs(final_score),
        lexical.get("intensity", 0),
        model.get("intensity", 0)
    )

    # --------------------------------------------------
    # Ironía
    # --------------------------------------------------

    irony = lexical.get("irony", False)

    # --------------------------------------------------
    # Emociones (priorizamos modelo)
    # --------------------------------------------------

    emotions = model.get("emotions", {})

    # --------------------------------------------------
    # EXPLICACIÓN COMPLETA
    # --------------------------------------------------

    explanations.extend(lexical.get("explanation", []))
    explanations.extend(model.get("explanation", []))

    # --------------------------------------------------
    # OUTPUT FINAL
    # --------------------------------------------------

    return {
        "polarity": final_polarity,
        "score": round(final_score, 3),
        "intensity": round(float(intensity), 3),
        "irony": irony,
        "emotions": emotions,
        "explanation": explanations
    }