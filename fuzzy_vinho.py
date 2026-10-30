"""Sistema de inferência fuzzy (Mamdani) para triagem de lotes de vinho tinto.

Dados: Wine Quality (vinho tinto), UCI Machine Learning Repository
Cortez et al. (2009). https://archive.ics.uci.edu/dataset/186/wine+quality
"""
import json
import numpy as np
import pandas as pd

# ------------------------------------------------------------------
# 1. Funções de pertinência (trapézios: a, b, c, d; triângulo = b == c)
# ------------------------------------------------------------------
def trap(x, a, b, c, d):
    x = np.asarray(x, dtype=float)
    up = np.where(b > a, (x - a) / (b - a + 1e-12), (x >= a).astype(float))
    down = np.where(d > c, (d - x) / (d - c + 1e-12), (x <= d).astype(float))
    return np.clip(np.minimum(np.minimum(up, 1.0), down), 0.0, 1.0)

VARS = {
    "alcool": {"label": "Teor alcoólico (% vol)", "col": "alcohol", "range": [8, 15],
               "termos": {"baixo": [8, 8, 9.5, 10.5], "medio": [9.5, 10.5, 10.5, 11.6],
                          "alto": [10.6, 11.8, 15, 15]}},
    "acidez": {"label": "Acidez volátil (g/L)", "col": "volatile acidity", "range": [0.1, 1.6],
               "termos": {"baixa": [0.1, 0.1, 0.35, 0.5], "media": [0.35, 0.58, 0.58, 0.95],
                          "alta": [0.7, 1.0, 1.6, 1.6]}},
    "sulfatos": {"label": "Sulfatos (g/L)", "col": "sulphates", "range": [0.3, 2.0],
                 "termos": {"baixo": [0.3, 0.3, 0.48, 0.6], "adequado": [0.55, 0.68, 0.85, 1.0],
                            "excessivo": [0.9, 1.1, 2.0, 2.0]}},
}
SAIDA = {"label": "Índice de qualidade (0–10)", "range": [0, 10],
         "termos": {"ruim": [2, 3, 3.5, 5], "regular": [4, 5.2, 5.2, 6.2],
                    "boa": [5.4, 6.4, 6.4, 7.4], "excelente": [6.6, 7.6, 9, 9]}}

# ------------------------------------------------------------------
# 2. Base de regras (antecedentes ligados por E = mínimo)
# ------------------------------------------------------------------
REGRAS = [
    ({"alcool": "alto", "acidez": "baixa"}, "excelente"),
    ({"alcool": "alto", "sulfatos": "adequado"}, "excelente"),
    ({"alcool": "alto", "acidez": "media"}, "boa"),
    ({"alcool": "medio", "acidez": "baixa", "sulfatos": "adequado"}, "boa"),
    ({"alcool": "medio", "acidez": "media"}, "regular"),
    ({"alcool": "medio", "sulfatos": "baixo"}, "regular"),
    ({"alcool": "baixo", "acidez": "baixa"}, "regular"),
    ({"alcool": "baixo", "acidez": "media"}, "regular"),
    ({"alcool": "baixo", "sulfatos": "baixo"}, "ruim"),
    ({"acidez": "alta"}, "ruim"),
    ({"sulfatos": "excessivo"}, "regular"),
]

Y = np.linspace(0, 10, 501)
MF_SAIDA = {t: trap(Y, *p) for t, p in SAIDA["termos"].items()}


def inferir(alcool, acidez, sulfatos, detalhes=False):
    entrada = {"alcool": alcool, "acidez": acidez, "sulfatos": sulfatos}
    # Fuzzificação
    mu = {v: {t: float(trap(entrada[v], *p)) for t, p in VARS[v]["termos"].items()} for v in VARS}
    # Avaliação das regras (min) e implicação de Mamdani (corte)
    agregado = np.zeros_like(Y)
    forcas = []
    for ant, cons in REGRAS:
        w = min(mu[v][t] for v, t in ant.items())
        forcas.append(w)
        agregado = np.maximum(agregado, np.minimum(w, MF_SAIDA[cons]))  # agregação (max)
    # Defuzzificação (centroide)
    if agregado.sum() == 0:
        y = 5.0
    else:
        y = float((Y * agregado).sum() / agregado.sum())
    if detalhes:
        return y, mu, forcas, agregado
    return y


def decisao(indice):
    if indice >= 6.6:
        return "Premium"
    if indice < 4.6:
        return "Revisar"
    return "Padrão"


def classe_real(q):
    return "Premium" if q >= 7 else ("Revisar" if q <= 4 else "Padrão")


if __name__ == "__main__":
    from scipy.stats import spearmanr

    df = pd.read_csv("data/winequality-red.csv", sep=";")
    df["indice"] = [inferir(a, v, s) for a, v, s in
                    zip(df["alcohol"], df["volatile acidity"], df["sulphates"])]
    df["decisao"] = df["indice"].map(decisao)
    df["real"] = df["quality"].map(classe_real)

    rho = spearmanr(df["indice"], df["quality"]).statistic
    print("Spearman índice fuzzy x nota:", round(rho, 3))
    for c in ["alcohol", "volatile acidity", "sulphates"]:
        print("  só", c, round(spearmanr(df[c], df["quality"]).statistic, 3))
    print(pd.crosstab(df["real"], df["decisao"]))
    print("acerto:", round((df.real == df.decisao).mean(), 3))
    print(df.groupby("quality")["indice"].agg(["mean", "median", "count"]).round(2))
    # Base: regra nítida (crisp) equivalente
    crisp = np.where((df.alcohol >= 11.5) & (df["volatile acidity"] < 0.5), "Premium",
                     np.where((df["volatile acidity"] >= 0.8) | ((df.alcohol < 9.5) & (df.sulphates < 0.5)),
                              "Revisar", "Padrão"))
    print("crisp:"); print(pd.crosstab(df.real, crisp)); print("acerto crisp:", round((df.real == crisp).mean(), 3))
