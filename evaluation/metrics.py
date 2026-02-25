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