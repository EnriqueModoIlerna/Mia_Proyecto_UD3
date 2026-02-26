"""
main.py
Ejecutor simple del analizador de sentimiento
"""

import json

from lexical.lexical_analyzer import analyze_lexical
from models.transformer_analyzer import analyze_model
from fusion.fusion_engine import fusion_results


def analyze_text(text):
    """
    Ejecuta el pipeline completo:
    léxico → modelo → fusión
    """

    # Análisis léxico
    lexical_result = analyze_lexical(text)

    # Análisis modelo
    try:
        model_result = analyze_model(text)
    except Exception:
        model_result = None

    # Fusión final
    final_result = fusion_results(lexical_result, model_result)

    return final_result


if __name__ == "__main__":

    print("=== ANALIZADOR DE SENTIMIENTO EN ESPAÑOL ===\n")

    text = input("Introduce una frase: ")

    result = analyze_text(text)

    print("\nResultado:\n")
    print(json.dumps(result, indent=4, ensure_ascii=False))