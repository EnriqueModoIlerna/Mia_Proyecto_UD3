# Proyecto UD3 – Análisis de Sentimiento (MIA)

Este proyecto corresponde a la **Unidad Didáctica 3** de la asignatura **MIA**, y tiene como objetivo implementar un **sistema de análisis de sentimiento** combinando distintos enfoques: análisis léxico, modelos basados en *transformers* y una estrategia de fusión de resultados.

El sistema permite analizar textos y clasificarlos según su polaridad sentimental, así como evaluar el rendimiento del modelo mediante métricas estándar.

---

## Estructura del proyecto
Mia_Proyecto_UD3/
│
├── data/
│ └── examples.csv # Ejemplos de texto para pruebas
│
├── lexical/
│ ├── lexical_analyzer.py # Analizador léxico principal
│ ├── negations.py # Gestión de negaciones
│ ├── intensifiers.py # Intensificadores léxicos
│ └── irony_rules.py # Reglas simples de ironía
│
├── models/
│ ├── transformer_analyzer.py # Analizador basado en transformers
│ └── model_utils.py # Utilidades comunes para modelos
│
├── fusion/
│ └── fusion_engine.py # Fusión de resultados léxico + modelo
│
├── evaluation/
│ └── metrics.py # Métricas de evaluación
│
├── main.py # Punto de entrada del proyecto
├── requirements.txt # Dependencias del proyecto
├── LICENSE # Licencia del proyecto


---

## Funcionamiento general

El flujo principal del sistema es el siguiente:

1. **Entrada de texto**  
   El texto a analizar se introduce desde el fichero `main.py` o desde un conjunto de ejemplos.

2. **Análisis léxico**  
   Se evalúa el texto teniendo en cuenta:
   - Palabras con polaridad positiva y negativa  
   - Negaciones  
   - Intensificadores  
   - Reglas simples de ironía  

3. **Análisis con modelo Transformer**  
   Se utiliza un modelo preentrenado para obtener una predicción basada en aprendizaje profundo.

4. **Fusión de resultados**  
   Ambos análisis se combinan mediante un motor de fusión para obtener una predicción final más robusta.

5. **Evaluación**  
   El módulo evaluation/metrics.py incluye funciones para calcular métricas típicas en análisis de sentimiento, como precisión, recall y F1-score, permitiendo evaluar el rendimiento del sistema sobre conjuntos de prueba.

***Tecnologías utilizadas***
Python 3

Modelos basados en Transformers

Técnicas de análisis léxico

Fusión de modelos

Evaluación mediante métricas estándar de clasificación
---

## Ejecución del proyecto

 Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Autores

Proyecto desarrollado por Alejandro Molina y Enrique Díaz como parte de la Unidad Didáctica 3 de la asignatura MIA.