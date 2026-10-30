# Lógica Fuzzy na prática: triagem de lotes de vinho

Página interativa sobre Lógica Fuzzy produzida para o **REVISA**, a plataforma de conteúdo da disciplina **Sistemas de Apoio à Decisão (SAD)** da Faculdade de Tecnologia da Unicamp (Limeira).

O trabalho apresenta a fundamentação teórica dos sistemas de inferência fuzzy e um estudo de caso com dados reais. Nele, um sistema Mamdani transforma três medições de laboratório num índice de qualidade e decide o destino de cada lote de vinho tinto: **Premium**, **Padrão** ou **Revisar** (prova sensorial).

## Conteúdo da página

- **Fundamentação teórica:** conjuntos fuzzy, funções de pertinência, variáveis linguísticas, operadores e as quatro etapas do método Mamdani (fuzzificação, avaliação de regras, agregação e defuzzificação por centroide).
- **Exemplo prático:** uma vinícola que precisa classificar 1.599 lotes reais de vinho tinto.
- **Implementação:** código Python com `scikit-fuzzy`, passo a passo.
- **Vantagens e limitações:** quando a técnica é adequada e quando preferir aprendizado de máquina.
- **Aplicação em SAD:** uso do índice nas decisões operacionais, gerenciais e estratégicas.

### Recursos interativos

- Animação que compara um conjunto nítido com um conjunto fuzzy.
- Laboratório que mostra as quatro etapas da inferência para qualquer lote. Dá para carregar vinhos reais do conjunto de dados.
- Gráfico com o índice fuzzy dos 1.599 vinhos, agrupados pela nota dos provadores.
- Superfícies de decisão do sistema fuzzy e de uma regra nítida, lado a lado.
- Painel do gerente: ajusta os limiares de decisão e atualiza a matriz de confusão e os indicadores na hora.

## Dados

**Wine Quality (vinho tinto)**, do [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/186/wine+quality): 1.599 amostras de vinho tinto, cada uma com 11 medições físico-químicas e a nota mediana de provadores (escala de 0 a 10).

> Cortez, P.; Cerdeira, A.; Almeida, F.; Matos, T.; Reis, J. (2009). Modeling wine preferences by data mining from physicochemical properties. *Decision Support Systems*, 47(4), 547–553.

As entradas do sistema são as três medições com maior correlação de Spearman com a nota:

| Variável | Spearman (ρ) | Termos linguísticos |
|---|---|---|
| Teor alcoólico | +0,48 | baixo, médio, alto |
| Acidez volátil | −0,38 | baixa, média, alta |
| Sulfatos | +0,38 | baixo, adequado, excessivo |

## O sistema fuzzy

- **Tipo:** Mamdani
- **Operadores:** E = mínimo, agregação = máximo
- **Defuzzificação:** centroide
- **Saída:** índice de qualidade de 0 a 10, com os termos ruim, regular, boa e excelente
- **Base de regras:** 11 regras escritas a partir de conhecimento especialista, sem nenhum parâmetro ajustado por treino

Limiares de decisão padrão (ajustáveis pelo gestor):

| Índice | Decisão |
|---|---|
| ≥ 6,6 | Premium |
| entre 4,6 e 6,6 | Padrão |
| < 4,6 | Revisar |

## Resultados

Aplicado aos 1.599 vinhos e comparado com as notas dos provadores, que o sistema nunca viu:

| Métrica | Valor |
|---|---|
| Correlação de Spearman (índice fuzzy x nota) | 0,55 (só o álcool chega a 0,48) |
| AUC para identificar vinhos com nota ≥ 7 | 0,85 |
| Vinhos nota ≥ 7 enviados ao Premium (recall) | 71 % |
| Lotes Premium que de fato têm nota ≥ 7 (precisão) | 41 % |

A precisão do Premium é baixa porque vinhos com nota 5 e 6 são muito parecidos nessas três medições. O painel gerencial da página serve justamente para explorar esse trade-off entre volume e precisão.

## Como executar

### Página

Abra `logica-fuzzy-revisa.html` em qualquer navegador. A página não precisa de servidor nem de instalação; só as fontes são carregadas do Google Fonts.

### Notebook e script

```bash
git clone https://github.com/<usuario>/logica-fuzzy-revisa.git
cd logica-fuzzy-revisa
pip install -r requirements.txt

# avaliação do sistema no terminal
python fuzzy_vinho.py

# notebook
jupyter notebook fuzzy_vinho_revisa.ipynb
```

Se o arquivo `data/winequality-red.csv` não estiver presente, o notebook baixa os dados direto da UCI.

## Tecnologias

- Python, NumPy, pandas, SciPy, scikit-learn, Matplotlib
- [scikit-fuzzy](https://github.com/scikit-fuzzy/scikit-fuzzy)
- HTML, CSS e JavaScript puro (gráficos em SVG e Canvas, sem bibliotecas)

## Referências

1. Zadeh, L. A. (1965). Fuzzy sets. *Information and Control*, 8(3), 338–353.
2. Mamdani, E. H.; Assilian, S. (1975). An experiment in linguistic synthesis with a fuzzy logic controller. *International Journal of Man-Machine Studies*, 7(1), 1–13.
3. Takagi, T.; Sugeno, M. (1985). Fuzzy identification of systems and its applications to modeling and control. *IEEE Transactions on Systems, Man, and Cybernetics*, 15(1), 116–132.
4. Cortez, P. et al. (2009). Modeling wine preferences by data mining from physicochemical properties. *Decision Support Systems*, 47(4), 547–553.
5. Turban, E.; Sharda, R.; Delen, D. (2011). *Decision Support and Business Intelligence Systems*. 9. ed. Pearson.

## Licença

Conteúdo produzido para fins educacionais na disciplina de Sistemas de Apoio à Decisão da FT Unicamp. O conjunto de dados Wine Quality é distribuído pela UCI sob a licença [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
