import json
import sys

# ===== PIPELINE =====
from lexical.lexical_analyzer import analyze_lexical
from models.transformer_analyzer import analyze_model
from fusion.fusion_engine import fusion_results

# ===== EVALUACIÓN =====
from evaluation.metrics import evaluate, save_report


# =====================================================
# FUNCIÓN PRINCIPAL DEL ANALIZADOR
# =====================================================
def analyze_text(text):
    """
    Ejecuta todo el pipeline:
    léxico → modelo → fusión
    """

    # análisis léxico
    lex = analyze_lexical(text)

    # análisis modelo
    try:
        mod = analyze_model(text)
    except NotImplementedError:
        mod = None

    # fusión
    final = fusion_results(lex, mod)

    return final


# =====================================================
# MODO INTERACTIVO
# =====================================================
def interactive_mode():
    text = input("Introduce una frase: ")
    result = analyze_text(text)

    print("\nResultado final:\n")
    print(json.dumps(result, indent=4, ensure_ascii=False))


# =====================================================
# MODO EVALUACIÓN AUTOMÁTICA
# =====================================================
def evaluation_mode():

    class AnalyzerWrapper:
        """
        Adaptador para usar evaluate()
        porque metrics espera .analyze(text)
        """

        def analyze(self, text):
            return analyze_text(text)

    analyzer = AnalyzerWrapper()

    results, examples = evaluate("data/examples.csv", analyzer)

    print("\nResultados evaluación:\n")
    print(json.dumps(results, indent=4))

    save_report(results, examples)

    print("\nReporte guardado como report.txt")


# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":

    # Si ejecutas:
    # python main.py eval
    if len(sys.argv) > 1 and sys.argv[1] == "eval":
        evaluation_mode()
    else:
        interactive_mode()