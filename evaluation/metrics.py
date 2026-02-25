from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
import pandas as pd

# =========================
# MÉTRICAS BÁSICAS
# =========================

def accuracy(y_true, y_pred):
    """Calcula accuracy"""
    return accuracy_score(y_true, y_pred)


def f1(y_true, y_pred, average="weighted"):
    """Calcula F1 score"""
    return f1_score(y_true, y_pred, average=average)


def get_confusion_matrix(y_true, y_pred):
    """Devuelve matriz de confusión"""
    return confusion_matrix(y_true, y_pred)


def full_report(y_true, y_pred):
    """Devuelve reporte completo de clasificación"""
    return classification_report(y_true, y_pred, digits=4)

# =========================
# EVALUACIÓN DEL ANALIZADOR
# =========================

def evaluate(csv_path, analyzer):
    """
    Evalúa el sistema completo usando dataset CSV

    Parameters
    ----------
    csv_path : str
        ruta al dataset
    analyzer : objeto
        clase principal de análisis con método analyze(text)

    Returns
    -------
    dict
        métricas calculadas
    """

    df = pd.read_csv(csv_path)

    if "texto" not in df.columns or "polaridad_real" not in df.columns:
        raise ValueError("El CSV debe tener columnas: texto, polaridad_real")

    y_true = []
    y_pred = []

    explanations = []

    for _, row in df.iterrows():
        text = row["texto"]
        real = row["polaridad_real"]

        result = analyzer.analyze(text)

        pred = result["polarity"]

        y_true.append(real)
        y_pred.append(pred)

        explanations.append({
            "texto": text,
            "real": real,
            "pred": pred,
            "explicacion": result.get("explanation", "")
        })

    # =========================
    # Cálculo métricas
    # =========================

    acc = accuracy(y_true, y_pred)
    f1score = f1(y_true, y_pred)
    matrix = get_confusion_matrix(y_true, y_pred)
    report = full_report(y_true, y_pred)

    results = {
        "accuracy": acc,
        "f1_score": f1score,
        "confusion_matrix": matrix.tolist(),
        "classification_report": report,
        "samples": len(y_true)
    }

    return results, explanations

