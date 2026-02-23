from lexical.lexical_analyzer import analyze_lexical
from models.transformer_analyzer import analyze_model
from fusion.fusion_engine import fusion_results

text = input("Introduce una frase: ")

lex = analyze_lexical(text)

try:
    mod = analyze_model(text)
except NotImplementedError:
    mod = None

final = fusion_results(lex, mod)
print(final)