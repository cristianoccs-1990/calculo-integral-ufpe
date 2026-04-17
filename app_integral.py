"""
Dashboard Interativo — Cálculo Integral
Matemática · Graduação · UFPE · 2026S1
Prof. Cristiano da Costa da Silva

Rodar: python3 app_integral.py
Acesse: http://localhost:8060
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc

# ── Paleta UFPE ──
BORDO   = "#9B2335"
BORDO_E = "#7A1A28"
DOURADO = "#D4A04A"
VERDE   = "#41801d"
AZUL    = "#1565c0"
CINZA   = "#333333"
VERMELHO = "#B50303"

# ── App ──
app = Dash(
    __name__,
    external_stylesheets=[],
    suppress_callback_exceptions=True,
    title="Cálculo Integral | Matemática UFPE",
    serve_locally=True,
)
server = app.server  # necessário para deploy (Gunicorn/Render)

PCFG = dict(
    displayModeBar=True, responsive=True,
    modeBarButtonsToRemove=["lasso2d", "select2d"],
    toImageButtonOptions=dict(format="png", height=800, width=1400),
)
FONT = dict(family="Open Sans, Helvetica, Arial", size=16, color=CINZA)

# ═══════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════

def navbar():
    return dbc.Navbar(
        dbc.Container([
            dbc.Row([
                dbc.Col(html.Img(src="/assets/logo_ufpe.png", height="38px"), width="auto"),
                dbc.Col(dbc.NavbarBrand("Matemática · Cálculo Integral",
                    style={"fontSize": "16px", "fontWeight": "700"}), width="auto"),
            ], align="center", className="g-2"),
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Panorama", href="/", active="exact")),
                dbc.NavItem(dbc.NavLink("Primitivas", href="/primitivas", active="exact")),
                dbc.NavItem(dbc.NavLink("Riemann", href="/riemann", active="exact")),
                dbc.NavItem(dbc.NavLink("TFC", href="/tfc", active="exact")),
                dbc.NavItem(dbc.NavLink("Áreas", href="/areas", active="exact")),
                dbc.NavItem(dbc.NavLink("Técnicas", href="/tecnicas", active="exact")),
                dbc.NavItem(dbc.NavLink("Frações Parciais", href="/fracoes-parciais", active="exact")),
                dbc.NavItem(dbc.NavLink("Aplicações", href="/aplicacoes", active="exact")),
                dbc.NavItem(dbc.NavLink("Exercícios", href="/exercicios", active="exact")),
            ], navbar=True, className="ms-auto"),
        ], fluid=True),
        color=BORDO, dark=True, sticky="top",
        style={"padding": "6px 0", "minHeight": "48px"},
    )

def section(title, children, hdr=BORDO):
    return dbc.Card([
        dbc.CardHeader(title, style={"background": hdr}),
        dbc.CardBody(children),
    ], className="mb-4")

def conceito(text):
    return html.Div(
        dcc.Markdown(text, dangerously_allow_html=True, mathjax=True),
        className="conceito-box",
    )

def eq_box(text):
    return html.Div(
        dcc.Markdown(text, dangerously_allow_html=True, mathjax=True),
        className="eq-box",
    )

def kpi(label, value, cor=BORDO):
    return dbc.Col(html.Div([
        html.Div(value, className="kpi-value", style={"color": cor}),
        html.Div(label, className="kpi-label"),
    ], className="kpi-box"), lg=3, md=6, className="mb-3")

def mario_question(question, answer):
    return html.Details([
        html.Summary(html.Div([
            html.Div("?", className="mario-question-icon"),
            html.Div(question, className="mario-question-text"),
        ], className="mario-question")),
        html.Div(
            dcc.Markdown(answer, dangerously_allow_html=True, mathjax=True),
            className="mario-answer",
        ),
    ], className="mario-details")

def mario_code(title, content):
    return html.Details([
        html.Summary(html.Div([
            html.Div("!", className="mario-code-icon"),
            html.Div(title, className="mario-code-text"),
        ], className="mario-code")),
        html.Div(
            dcc.Markdown(content, dangerously_allow_html=True, mathjax=True),
            className="mario-code-detail",
        ),
    ], className="mario-details")

def footer():
    return html.Div(
        "Matemática · Prof. Cristiano da Costa da Silva · UFPE · 2026S1",
        className="footer-text",
    )

def wrap(children):
    return html.Div(children, className="main-content")

def obs_box(text):
    return html.Div(
        dcc.Markdown(text, dangerously_allow_html=True, mathjax=True),
        className="obs-box",
    )

# ═══════════════════════════════════════════
#  PÁGINA 1 — PANORAMA
# ═══════════════════════════════════════════

def pg_panorama():
    return wrap([
        html.H3("Panorama da Aula — Cálculo Integral"),
        html.Hr(),
        dbc.Row([
            kpi("Blocos", "10"),
            kpi("Exercícios", "10", DOURADO),
            kpi("Equações", "~50", AZUL),
            kpi("Gráficos Interativos", "8", VERDE),
        ]),

        section("Visão Geral", [
            dcc.Markdown(r"""
A integral é a segunda operação fundamental do Cálculo, complementar à derivação.
Enquanto a derivada mede a taxa de variação instantânea, a integral permite
**acumular quantidades que variam continuamente**.

Na Economia, esse problema surge naturalmente: conhecemos o custo marginal $C'(q)$
e queremos o custo total $C(q)$; conhecemos a curva de demanda e queremos o
excedente do consumidor. Em Física, conhecemos a velocidade e queremos a posição.
Em Geometria, queremos a área de regiões com bordas curvas. A integral resolve
todos esses problemas com a mesma estrutura matemática.
            """, mathjax=True),
        ]),

        section("Contexto Histórico", [
            dcc.Markdown(r"""
O problema de calcular áreas de figuras curvas remonta à Antiguidade:

- **Arquimedes (287 a 212 a.C.)** calculou a área sob uma parábola dividindo-a em
triângulos cada vez menores e mostrou que a área sob $y = x^2$ entre $0$ e $1$ vale $\frac{1}{3}$.

- **Newton (1643 a 1727) e Leibniz (1646 a 1716)**, trabalhando independentemente,
formalizaram o Cálculo no século XVII. Leibniz criou o símbolo $\int$, um "S"
alongado representando *summa* (soma em latim).

- **Riemann (1826 a 1866)** estabeleceu a definição rigorosa que utilizamos hoje:
a integral como limite de somas de retângulos.

O símbolo $\int_a^b f(x)\,dx$ lê-se *"a integral de $f(x)$ de $a$ até $b$"*.
            """, mathjax=True),
        ]),

        section("Aplicações em Economia", [
            dcc.Markdown(r"""
A integral conecta **grandezas marginais** (derivadas) a **grandezas totais** (acumulados):

| Grandeza Marginal (derivada) | Grandeza Total (integral) |
|:---|:---|
| Custo Marginal $C'(q)$ | Custo Total $C(q) = \int C'(q)\,dq + C_0$ |
| Receita Marginal $R'(q)$ | Receita Total $R(q) = \int R'(q)\,dq$ |
| Taxa de juros instantânea $r(t)$ | Fator de capitalização $e^{\int r(t)\,dt}$ |
| Função demanda inversa $p = f(q)$ | Excedente do Consumidor $EC = \int_0^{q^*} f(q)\,dq - p^*q^*$ |

**Simon & Blume** (*Mathematics for Economists*, Cap. 17):
> *"A integral indefinida desfaz o que a derivada faz. Se sabemos a taxa marginal
> de variação de uma quantidade econômica, a integração nos devolve a quantidade total."*
            """, mathjax=True),
        ], hdr=BORDO_E),

        section("Roteiro da Aula", [
            dcc.Markdown(r"""
**1. Primitivas** — Processo inverso da derivação: dado $f'(x) = 2x$, encontrar $f(x) = x^2 + C$

**2. Integral de Riemann** — Cálculo de áreas sob curvas via somas de retângulos

**3. Teorema Fundamental do Cálculo** — Conexão entre primitiva e integral definida:
$\int_a^b f(x)\,dx = F(b) - F(a)$

**4. Cálculo de Áreas** — Aplicação do TFC para áreas entre curvas

**5. Técnicas de Integração** — Substituição e integração por partes

**6. Frações Parciais** — Integração de funções racionais $P(x)/Q(x)$

**7. Aplicações Econômicas** — Valor presente, tempo ótimo, excedente do consumidor, custo e receita
            """, mathjax=True),
        ]),

        section("Referências", [
            html.P("Guidorizzi, H. L. — Um Curso de Cálculo, Vol. 1, 5ª ed. (Caps. 10, 11 e 12)"),
            html.P("Simon, C. & Blume, L. — Mathematics for Economists (Caps. 17 e 18)"),
        ]),

        footer(),
    ])

# ═══════════════════════════════════════════
#  PÁGINA 2 — PRIMITIVAS
# ═══════════════════════════════════════════

def pg_primitivas():
    return wrap([
        html.H3("Primitivas (Antiderivadas)"),
        html.Hr(),

        section("Objetivo", [
            conceito(r"""
**Objetivo:** A primitiva realiza o processo inverso da derivação. Dada a taxa de variação
$f(x)$, encontrar a função original $F(x)$ tal que $F'(x) = f(x)$.
Em Economia, permite recuperar o custo total a partir do custo marginal, a receita total
a partir da receita marginal, entre outras aplicações.
            """),
        ], hdr=BORDO_E),

        section("O que é uma Primitiva?", [
            conceito(r"""
**Definição:** Uma **primitiva** (ou antiderivada) de $f$ em um intervalo $I$ é uma função $F$
definida em $I$ tal que $F'(x) = f(x)$ para todo $x$ em $I$.

A notação $\displaystyle\int f(x)\,dx$ representa a família de todas as primitivas de $f$.
            """),
        ]),

        section("Teorema: A Primitiva Geral", [
            eq_box(r"""
Se $F$ é uma primitiva de $f$ em um intervalo $I$, então a primitiva mais geral de $f$ em $I$ é:
$$\int f(x)\,dx = F(x) + C$$
onde $C$ é uma constante arbitrária.
            """),
            dcc.Markdown(r"""
**Por que a constante $C$?** Porque se $F'(x) = f(x)$, então $(F(x) + 5)' = f(x)$ também,
e $(F(x) - 100)' = f(x)$, etc. Qualquer constante somada desaparece na derivação.
A constante $C$ captura essa ambiguidade: há infinitas primitivas, todas diferindo por uma constante.
            """, mathjax=True),
            mario_code("Demonstração: por que todas as primitivas diferem por uma constante", r"""
**Objetivo:** Mostrar que se $F$ e $G$ são ambas primitivas de $f$ em $I$, então $G(x) = F(x) + C$.

**Passo 1:** Defina $h(x) = G(x) - F(x)$. Então:
$$h'(x) = G'(x) - F'(x) = f(x) - f(x) = 0 \quad \text{para todo } x \in I$$

**Passo 2:** Uma função cuja derivada é zero em todo ponto de um intervalo é constante.
(Isso é consequência do Teorema do Valor Médio, já visto na aula de derivadas.)

**Passo 3:** Logo $h(x) = C$ (constante), ou seja:
$$G(x) - F(x) = C \implies G(x) = F(x) + C \qquad \blacksquare$$
            """),
        ]),

        section("Regras Básicas de Integração", [
            dcc.Markdown(r"""
Cada regra de integração é obtida "invertendo" uma regra de derivação conhecida.
Para cada uma, basta verificar: *a derivada do resultado é o integrando?*
            """, mathjax=True),

            html.H5("Regra 1: Integral de uma constante"),
            eq_box(r"""$$\int c\,dx = cx + C$$"""),
            mario_code("Demonstração: Regra da constante", r"""
Precisamos encontrar $F(x)$ tal que $F'(x) = c$ (constante).

Sabemos que $(cx)' = c$. Logo: $\displaystyle\int c\,dx = cx + C \qquad \blacksquare$

**Exemplo:** $\displaystyle\int 7\,dx = 7x + C$
            """),

            html.H5("Regra 2: Integral da potência", className="mt-4"),
            eq_box(r"""
$$\int x^n\,dx = \frac{x^{n+1}}{n+1} + C \qquad (n \neq -1)$$
            """),
            mario_code("Demonstração: Regra da potência", r"""
Precisamos encontrar $F(x)$ tal que $F'(x) = x^n$.

**Candidato:** $F(x) = \dfrac{x^{n+1}}{n+1}$.

**Verificação:** $F'(x) = \dfrac{(n+1)\,x^n}{n+1} = x^n$ ✓

Logo: $\displaystyle\int x^n\,dx = \frac{x^{n+1}}{n+1} + C$, válido para $n \neq -1$. $\qquad \blacksquare$

**Exemplos:**

- $\displaystyle\int x^2\,dx = \frac{x^3}{3} + C$

- $\displaystyle\int x^5\,dx = \frac{x^6}{6} + C$

- $\displaystyle\int \frac{1}{x^3}\,dx = \int x^{-3}\,dx = \frac{x^{-2}}{-2} + C = -\frac{1}{2x^2} + C$

- $\displaystyle\int \sqrt{x}\,dx = \int x^{1/2}\,dx = \frac{x^{3/2}}{3/2} + C = \frac{2}{3}x\sqrt{x} + C$
            """),

            html.H5("Regra 3: Integral de 1/x", className="mt-4"),
            eq_box(r"""$$\int \frac{1}{x}\,dx = \ln|x| + C \qquad (x \neq 0)$$"""),
            mario_code("Demonstração: por que 1/x é um caso especial", r"""
A regra da potência $\int x^n dx = \frac{x^{n+1}}{n+1}$ **não funciona** quando $n = -1$,
pois teríamos divisão por zero: $\frac{x^0}{0}$.

Precisamos de outra abordagem. Sabemos da aula de derivadas que:
$$(\ln x)' = \frac{1}{x} \quad \text{para } x > 0$$

E que $(\ln(-x))' = \frac{1}{-x} \cdot (-1) = \frac{1}{x}$ para $x < 0$.

Combinando: $(\ln|x|)' = \frac{1}{x}$ para todo $x \neq 0$.

Logo: $\displaystyle\int \frac{1}{x}\,dx = \ln|x| + C \qquad \blacksquare$
            """),

            html.H5("Regra 4: Integral da exponencial", className="mt-4"),
            eq_box(r"""$$\int e^x\,dx = e^x + C$$"""),
            mario_code("Demonstração: Integral da exponencial", r"""
Sabemos que $(e^x)' = e^x$. Logo a exponencial é primitiva de si mesma:

$$\int e^x\,dx = e^x + C \qquad \blacksquare$$

**Generalização:** Para $\alpha \neq 0$:
$$\int e^{\alpha x}\,dx = \frac{e^{\alpha x}}{\alpha} + C$$

**Verificação:** $\left(\dfrac{e^{\alpha x}}{\alpha}\right)' = \dfrac{\alpha\,e^{\alpha x}}{\alpha} = e^{\alpha x}$ ✓

**Exemplo:** $\displaystyle\int e^{3x}\,dx = \frac{e^{3x}}{3} + C$
            """),

            html.H5("Regra 5: Integral da exponencial de base a", className="mt-4"),
            eq_box(r"""$$\int a^x\,dx = \frac{a^x}{\ln a} + C \qquad (a > 0,\; a \neq 1)$$"""),
            mario_code("Demonstração: Integral de a^x", r"""
Sabemos que $(a^x)' = a^x \cdot \ln a$. Logo:

$$\left(\frac{a^x}{\ln a}\right)' = \frac{a^x \cdot \ln a}{\ln a} = a^x$$

Portanto: $\displaystyle\int a^x\,dx = \frac{a^x}{\ln a} + C \qquad \blacksquare$

**Exemplo:** $\displaystyle\int 2^x\,dx = \frac{2^x}{\ln 2} + C \approx \frac{2^x}{0{,}693} + C$
            """),
        ]),

        section("Propriedades da Integral Indefinida", [
            eq_box(r"""
**Linearidade:** Para quaisquer constantes $\alpha, \beta$ e funções $f, g$:
$$\int \big[\alpha\,f(x) + \beta\,g(x)\big]\,dx = \alpha\int f(x)\,dx + \beta\int g(x)\,dx$$
            """),
            mario_code("Demonstração: Linearidade da integral", r"""
Seja $F$ primitiva de $f$ e $G$ primitiva de $g$. Então:
$$\big[\alpha F(x) + \beta G(x)\big]' = \alpha F'(x) + \beta G'(x) = \alpha f(x) + \beta g(x)$$

Logo $\alpha F + \beta G$ é primitiva de $\alpha f + \beta g$. $\qquad \blacksquare$

**Em palavras:** a integral de uma soma é a soma das integrais,
e constantes multiplicativas "saem" da integral.

**Exemplo:**
$$\int (3x^2 + 5e^x - \frac{4}{x})\,dx = 3 \cdot \frac{x^3}{3} + 5e^x - 4\ln|x| + C = x^3 + 5e^x - 4\ln|x| + C$$
            """),
        ]),

        section("Tabela de Primitivas Imediatas", [
            dcc.Markdown(r"""
| Função $f(x)$ | Primitiva $\int f(x)\,dx$ | Verificação |
|:---:|:---:|:---:|
| $c$ (constante) | $cx + C$ | $(cx)' = c$ ✓ |
| $x^n \;(n \neq -1)$ | $\dfrac{x^{n+1}}{n+1} + C$ | $\left(\dfrac{x^{n+1}}{n+1}\right)' = x^n$ ✓ |
| $\dfrac{1}{x}$ | $\ln\|x\| + C$ | $(\ln\|x\|)' = \dfrac{1}{x}$ ✓ |
| $e^x$ | $e^x + C$ | $(e^x)' = e^x$ ✓ |
| $e^{\alpha x}$ | $\dfrac{e^{\alpha x}}{\alpha} + C$ | $\left(\dfrac{e^{\alpha x}}{\alpha}\right)' = e^{\alpha x}$ ✓ |
| $a^x \;(a > 0, a\neq 1)$ | $\dfrac{a^x}{\ln a} + C$ | $\left(\dfrac{a^x}{\ln a}\right)' = a^x$ ✓ |
            """, mathjax=True),
            obs_box(r"""
**Dica prática:** Sempre verifique seu resultado derivando. Se a derivada da sua
resposta é igual ao integrando, a conta está certa!
            """),
        ]),

        section("Problema de Valor Inicial (PVI)", [
            dcc.Markdown(r"""
Muitas vezes, além de encontrar a primitiva geral, precisamos determinar a constante $C$
usando uma **condição inicial** — um valor conhecido de $F$ em algum ponto.
            """, mathjax=True),

            dcc.Markdown(r"""
**Exemplo 1 (Cinemática):** Uma partícula desloca-se com velocidade $v(t) = 2t + 1$ e
posição inicial $x(0) = 1$. Determine $x(t)$.

**Solução:**
$$x(t) = \int v(t)\,dt = \int (2t + 1)\,dt = t^2 + t + C$$

Usando $x(0) = 1$: $\;0 + 0 + C = 1 \implies C = 1$

$$\boxed{x(t) = t^2 + t + 1}$$
            """, mathjax=True),

            dcc.Markdown(r"""
**Exemplo 2 (Economia — Simon & Blume):** O custo marginal de uma empresa é $C'(q) = 6q + 4$
e o custo fixo é $C(0) = 200$. Encontre o custo total.

**Solução:**
$$C(q) = \int (6q + 4)\,dq = 3q^2 + 4q + C_0$$

Usando $C(0) = 200$: $\;C_0 = 200$.

$$\boxed{C(q) = 3q^2 + 4q + 200}$$

**Interpretação:** Para produzir $q = 10$ unidades: $C(10) = 300 + 40 + 200 = 540$ u.m.
O custo fixo de 200 (aluguel, equipamentos) é recuperado pela constante de integração.
            """, mathjax=True),
        ]),

        footer(),
    ])

# ═══════════════════════════════════════════
#  PÁGINA 3 — INTEGRAL DE RIEMANN
# ═══════════════════════════════════════════

def pg_riemann():
    return wrap([
        html.H3("Integral de Riemann"),
        html.Hr(),

        section("Objetivo", [
            conceito(r"""
**Objetivo:** Formalizar o cálculo de áreas sob curvas. A integral de Riemann define a
área como limite de somas de retângulos, permitindo calcular áreas de regiões com bordas
curvas para as quais não existem fórmulas geométricas elementares.
            """),
        ], hdr=BORDO_E),

        section("A Ideia Central: Aproximação por Retângulos", [
            dcc.Markdown(r"""
O procedimento de Riemann consiste em quatro etapas:

1. **Dividir** o intervalo $[a, b]$ em $n$ subintervalos
2. **Aproximar** a área sob a curva pela soma das áreas de $n$ retângulos
3. **Refinar** a partição, aumentando $n$
4. **Tomar o limite** quando $n \to \infty$, obtendo a área exata
            """, mathjax=True),
        ]),

        section("Partição de um Intervalo", [
            conceito(r"""
**Definição:** Uma **partição** $P$ de $[a, b]$ é um conjunto finito de pontos:
$$P = \{x_0, x_1, x_2, \ldots, x_n\} \quad\text{com}\quad a = x_0 < x_1 < x_2 < \cdots < x_n = b$$

Cada subintervalo $[x_{i-1}, x_i]$ tem **amplitude** (largura) $\Delta x_i = x_i - x_{i-1}$.
            """),
            dcc.Markdown(r"""
**Exemplo:** Uma partição de $[0, 1]$ em 4 partes iguais:
$$P = \{0;\; 0{,}25;\; 0{,}5;\; 0{,}75;\; 1\}, \quad \Delta x_i = 0{,}25 \text{ para todo } i$$
            """, mathjax=True),
        ]),

        section("Soma de Riemann", [
            conceito(r"""
**Definição:** Dada $f$ definida em $[a,b]$, uma partição $P$ e pontos $c_i \in [x_{i-1}, x_i]$
escolhidos arbitrariamente, a **Soma de Riemann** é:
$$S(f, P) = \sum_{i=1}^{n} f(c_i)\,\Delta x_i = f(c_1)\Delta x_1 + f(c_2)\Delta x_2 + \cdots + f(c_n)\Delta x_n$$
            """),
            dcc.Markdown(r"""
**O que cada parcela representa?**

Cada termo $f(c_i) \cdot \Delta x_i$ é a **área de um retângulo** com:
- **base** = $\Delta x_i$ (largura do subintervalo)
- **altura** = $f(c_i)$ (valor da função em algum ponto do subintervalo)

Se $f(c_i) > 0$: o retângulo tem área positiva (acima do eixo $x$).
Se $f(c_i) < 0$: contribui negativamente (abaixo do eixo $x$).

**A soma de todos os retângulos aproxima a área sob a curva.**

A escolha dos $c_i$ pode ser:
- **Extremo esquerdo:** $c_i = x_{i-1}$
- **Extremo direito:** $c_i = x_i$
- **Ponto médio:** $c_i = \frac{x_{i-1} + x_i}{2}$ (geralmente a melhor aproximação)
            """, mathjax=True),
        ]),

        section("Gráfico Interativo: Soma de Riemann", [
            conceito(r"""
A soma $S_n = \sum_{i=1}^n f(c_i)\Delta x_i$ converge para a área exata quando $n$ aumenta.
Aumente $n$ e observe o erro diminuir.
            """),
            dbc.Row([
                dbc.Col([
                    html.Label("Número de retângulos (n):", style={"fontWeight": "600"}),
                    dcc.Slider(id="slider-riemann-n", min=2, max=100, step=1, value=10,
                        marks={2: "2", 10: "10", 25: "25", 50: "50", 100: "100"},
                        tooltip={"placement": "bottom"}),
                ], md=4),
                dbc.Col([
                    html.Label("Função:", style={"fontWeight": "600"}),
                    dcc.Dropdown(id="dropdown-riemann-func",
                        options=[
                            {"label": "f(x) = x²", "value": "x2"},
                            {"label": "f(x) = x³", "value": "x3"},
                            {"label": "f(x) = e^(-x)", "value": "expnx"},
                            {"label": "f(x) = √x", "value": "sqrtx"},
                        ], value="x2", clearable=False),
                ], md=4),
                dbc.Col([
                    html.Label("Tipo de soma:", style={"fontWeight": "600"}),
                    dcc.Dropdown(id="dropdown-riemann-tipo",
                        options=[
                            {"label": "Extremo esquerdo", "value": "esq"},
                            {"label": "Extremo direito", "value": "dir"},
                            {"label": "Ponto médio", "value": "med"},
                        ], value="esq", clearable=False),
                ], md=4),
            ]),
            dcc.Graph(id="graph-riemann", config=PCFG),
        ]),

        section("Definição Formal da Integral de Riemann", [
            eq_box(r"""
$$\int_a^b f(x)\,dx = \lim_{\max \Delta x_i \to 0} \sum_{i=1}^{n} f(c_i)\,\Delta x_i$$

Se este limite existir (e não depender da escolha dos $c_i$), dizemos que $f$ é
**integrável** (no sentido de Riemann) em $[a,b]$.
            """),
            obs_box(r"""
**Fato importante (admitido sem demonstração):** Toda função contínua em $[a,b]$ é integrável
em $[a,b]$. Ou seja, para funções contínuas, o limite acima sempre existe.
Não demonstraremos este fato, pois a prova exige técnicas avançadas de Análise Real.
            """),
        ]),

        section("Propriedades da Integral Definida", [
            dcc.Markdown(r"""
Sejam $f$ e $g$ integráveis em $[a,b]$ e $k$ uma constante real:
            """, mathjax=True),
            eq_box(r"""
**a) Linearidade (soma):** $\displaystyle\int_a^b [f(x) + g(x)]\,dx = \int_a^b f(x)\,dx + \int_a^b g(x)\,dx$

**b) Linearidade (escalar):** $\displaystyle\int_a^b k\cdot f(x)\,dx = k\int_a^b f(x)\,dx$

**c) Positividade:** Se $f(x) \geq 0$ em $[a,b]$, então $\displaystyle\int_a^b f(x)\,dx \geq 0$

**d) Aditividade:** Se $c \in (a,b)$: $\displaystyle\int_a^b f(x)\,dx = \int_a^c f(x)\,dx + \int_c^b f(x)\,dx$

**e) Inversão de limites:** $\displaystyle\int_a^b f(x)\,dx = -\int_b^a f(x)\,dx$
            """),
            mario_code("Demonstração: propriedade (a) — Linearidade", r"""
Pela definição de integral como limite de somas de Riemann:

$$\int_a^b [f(x)+g(x)]\,dx = \lim \sum_{i=1}^n [f(c_i)+g(c_i)]\,\Delta x_i$$

$$= \lim \left[\sum_{i=1}^n f(c_i)\,\Delta x_i + \sum_{i=1}^n g(c_i)\,\Delta x_i\right]$$

$$= \lim \sum f(c_i)\,\Delta x_i + \lim \sum g(c_i)\,\Delta x_i$$

$$= \int_a^b f(x)\,dx + \int_a^b g(x)\,dx \qquad \blacksquare$$
            """),
            mario_code("Demonstração: propriedade (d) — Aditividade", r"""
Intuitivamente: se $c$ está entre $a$ e $b$, podemos dividir a "soma total" em duas partes
— de $a$ até $c$ e de $c$ até $b$. Formalmente:

Seja $P_1$ uma partição de $[a,c]$ e $P_2$ uma partição de $[c,b]$.
Então $P = P_1 \cup P_2$ é uma partição de $[a,b]$, e:

$$\sum_{P} f(c_i)\Delta x_i = \sum_{P_1} f(c_i)\Delta x_i + \sum_{P_2} f(c_i)\Delta x_i$$

Passando ao limite quando $\max \Delta x_i \to 0$:

$$\int_a^b f(x)\,dx = \int_a^c f(x)\,dx + \int_c^b f(x)\,dx \qquad \blacksquare$$
            """),
        ]),

        section("Gráfico Interativo: Aproximação Poligonal do Círculo", [
            conceito(r"""
Polígono regular de $n$ lados inscrito no círculo de raio 1. A área do polígono
$A_n = \frac{n}{2}\,\text{sen}(2\pi/n)$ converge para $\pi$ quando $n$ cresce.
Mesma lógica da soma de Riemann: mais subdivisões, melhor aproximação.
            """),
            dbc.Row([
                dbc.Col([
                    html.Label("Número de lados:", style={"fontWeight": "600"}),
                    dcc.Slider(id="slider-poligono-n", min=3, max=50, step=1, value=4,
                        marks={3: "3", 4: "4", 5: "5", 6: "6", 8: "8", 10: "10",
                               12: "12", 20: "20", 30: "30", 50: "50"},
                        tooltip={"placement": "bottom"}),
                ], md=8),
            ]),
            dcc.Graph(id="graph-poligono", config=PCFG),
        ]),

        footer(),
    ])

# ═══════════════════════════════════════════
#  PÁGINA 4 — TEOREMA FUNDAMENTAL DO CÁLCULO
# ═══════════════════════════════════════════

def pg_tfc():
    return wrap([
        html.H3("1.º Teorema Fundamental do Cálculo"),
        html.Hr(),

        section("Objetivo", [
            conceito(r"""
**Objetivo:** Estabelecer a conexão entre primitivas (problema algébrico) e a integral
de Riemann (problema geométrico). O TFC mostra que $\int_a^b f(x)\,dx = F(b) - F(a)$,
permitindo calcular integrais definidas sem recorrer a somas de retângulos.
            """),
        ], hdr=BORDO_E),

        section("Dois Problemas, Uma Resposta", [
            dcc.Markdown(r"""
Até aqui, tratamos dois problemas de natureza distinta:

1. **Primitivas:** encontrar $F$ tal que $F' = f$ (problema algébrico)
2. **Integral de Riemann:** calcular $\int_a^b f(x)\,dx$ como limite de somas (problema geométrico)

O TFC mostra que esses dois problemas estão conectados: para calcular a integral
definida, basta encontrar uma primitiva e avaliar nos extremos do intervalo.
            """, mathjax=True),
        ]),

        eq_box(r"""
**1.º Teorema Fundamental do Cálculo:** Se $f$ for integrável em $[a,b]$ e $F$ for uma
primitiva de $f$ em $[a,b]$ (ou seja, $F' = f$), então:
$$\int_a^b f(x)\,dx = F(b) - F(a) = \Big[F(x)\Big]_a^b$$
        """),

        mario_code("Demonstração do 1.º TFC (via Teorema do Valor Médio)", r"""
**Passo 1 — Telescópio:** Seja $P = \{x_0, x_1, \ldots, x_n\}$ uma partição de $[a,b]$.
O acréscimo total de $F$ pode ser escrito como soma telescópica:
$$F(b) - F(a) = \sum_{i=1}^{n} \big[F(x_i) - F(x_{i-1})\big]$$
(Os termos intermediários se cancelam: $F(x_1) - F(x_0) + F(x_2) - F(x_1) + \cdots$)

**Passo 2 — TVM:** Pelo **Teorema do Valor Médio**, para cada subintervalo $[x_{i-1}, x_i]$,
existe um ponto $\bar{c}_i \in (x_{i-1}, x_i)$ tal que:
$$F(x_i) - F(x_{i-1}) = F'(\bar{c}_i) \cdot (x_i - x_{i-1})$$

**Passo 3 — Usar $F' = f$:** Como $F' = f$, temos $F'(\bar{c}_i) = f(\bar{c}_i)$ e $x_i - x_{i-1} = \Delta x_i$:
$$F(b) - F(a) = \sum_{i=1}^{n} f(\bar{c}_i)\,\Delta x_i$$

**Passo 4 — Reconhecer a soma de Riemann:** O lado direito é exatamente uma soma de Riemann!
Tomando o limite quando $\max \Delta x_i \to 0$:
$$F(b) - F(a) = \lim_{\max \Delta x_i \to 0} \sum_{i=1}^{n} f(\bar{c}_i)\,\Delta x_i = \int_a^b f(x)\,dx \qquad \blacksquare$$

**Em palavras:** o TFC nos diz que a integral (soma de infinitas parcelas) pode ser calculada
simplesmente avaliando a primitiva nos extremos do intervalo.
        """),

        section("Exemplos Resolvidos", [
            dcc.Markdown(r"""
**Exemplo 1:** $\displaystyle\int_1^2 x^2\,dx$

Primitiva de $x^2$: $F(x) = \dfrac{x^3}{3}$

$$\int_1^2 x^2\,dx = \left[\frac{x^3}{3}\right]_1^2 = \frac{2^3}{3} - \frac{1^3}{3} = \frac{8}{3} - \frac{1}{3} = \boxed{\frac{7}{3} \approx 2{,}333}$$
            """, mathjax=True),

            dcc.Markdown(r"""
**Exemplo 2:** $\displaystyle\int_0^2 (x^3 + 3x - 1)\,dx$

Primitiva: $F(x) = \dfrac{x^4}{4} + \dfrac{3x^2}{2} - x$

$$\left[\frac{x^4}{4} + \frac{3x^2}{2} - x\right]_0^2 = \left(\frac{16}{4} + \frac{12}{2} - 2\right) - (0) = 4 + 6 - 2 = \boxed{8}$$
            """, mathjax=True),

            dcc.Markdown(r"""
**Exemplo 3:** $\displaystyle\int_1^2 \frac{1}{x^2}\,dx$

Reescrevemos: $\frac{1}{x^2} = x^{-2}$. Primitiva: $F(x) = \frac{x^{-1}}{-1} = -\frac{1}{x}$

$$\left[-\frac{1}{x}\right]_1^2 = -\frac{1}{2} - \left(-1\right) = -\frac{1}{2} + 1 = \boxed{\frac{1}{2}}$$
            """, mathjax=True),

            dcc.Markdown(r"""
**Exemplo 4:** $\displaystyle\int_0^1 e^{-x}\,dx$

Primitiva de $e^{-x}$: $F(x) = -e^{-x}$ (pois $(-e^{-x})' = e^{-x}$)

$$\left[-e^{-x}\right]_0^1 = -e^{-1} - (-e^0) = -\frac{1}{e} + 1 = \boxed{1 - \frac{1}{e} \approx 0{,}632}$$
            """, mathjax=True),

            dcc.Markdown(r"""
**Exemplo 5:** $\displaystyle\int_1^e \frac{1}{x}\,dx$

Primitiva de $\frac{1}{x}$: $F(x) = \ln x$ (para $x > 0$)

$$\left[\ln x\right]_1^e = \ln e - \ln 1 = 1 - 0 = \boxed{1}$$

**Interpretação geométrica:** A área sob a hipérbole $y = 1/x$ de $1$ até $e \approx 2{,}718$ vale exatamente 1.
            """, mathjax=True),
        ]),

        section("Verificação Numérica: Soma de Riemann vs TFC", [
            dcc.Markdown(r"""
Para confirmar o TFC, comparemos a soma de Riemann (ponto médio) com o valor exato
para $\displaystyle\int_0^1 x^2\,dx = \frac{1}{3} \approx 0{,}33333$:

| $n$ (retângulos) | Soma de Riemann | Erro absoluto | Erro relativo |
|:---:|:---:|:---:|:---:|
| 4 | 0,32813 | 0,00521 | 1,56% |
| 10 | 0,33250 | 0,00083 | 0,25% |
| 100 | 0,33333 | 8,3 × 10⁻⁶ | 0,0025% |
| 1.000 | 0,33333 | 8,3 × 10⁻⁸ | 0,000025% |

O TFC nos dá o resultado **exato** com uma única conta: $\frac{1^3}{3} - \frac{0^3}{3} = \frac{1}{3}$.
Sem o TFC, precisaríamos de milhares de retângulos para uma boa aproximação!
            """, mathjax=True),
        ]),

        footer(),
    ])

# ═══════════════════════════════════════════
#  PÁGINA 5 — CÁLCULO DE ÁREAS
# ═══════════════════════════════════════════

def pg_areas():
    return wrap([
        html.H3("Cálculo de Áreas"),
        html.Hr(),

        section("Área sob uma Curva", [
            dcc.Markdown(r"""
A interpretação geométrica mais natural da integral é o **cálculo de áreas**.
Distinguimos três situações:
            """, mathjax=True),

            conceito(r"""
**Caso 1 — $f(x) \geq 0$:** A área da região entre $y = f(x)$, $y = 0$, $x = a$ e $x = b$ é:
$$A = \int_a^b f(x)\,dx$$
            """),
            conceito(r"""
**Caso 2 — $f(x) \leq 0$:** Como a integral será negativa, a área (sempre positiva) é:
$$A = -\int_a^b f(x)\,dx = \int_a^b \big[-f(x)\big]\,dx$$
            """),
            conceito(r"""
**Caso 3 — $f$ muda de sinal:** Usamos o valor absoluto:
$$A = \int_a^b |f(x)|\,dx$$
Na prática, dividimos o intervalo nos pontos onde $f$ se anula e somamos as áreas parciais.
            """),
        ]),

        section("Área entre Duas Curvas", [
            eq_box(r"""
Se $f(x) \geq g(x)$ em $[a,b]$, a área da região entre as duas curvas é:
$$A = \int_a^b \big[f(x) - g(x)\big]\,dx$$
            """),
            mario_code("Por que f(x) - g(x)?", r"""
A ideia é simples: a área entre duas curvas é a diferença entre duas áreas:

$$A_{\text{entre}} = A_{\text{sob } f} - A_{\text{sob } g} = \int_a^b f(x)\,dx - \int_a^b g(x)\,dx$$

Pela linearidade da integral:

$$= \int_a^b [f(x) - g(x)]\,dx \qquad \blacksquare$$
            """),
        ]),

        section("Exemplos Resolvidos", [
            dcc.Markdown(r"""
**Exemplo 1:** Área sob $y = x^2$ de $0$ a $1$:
$$A = \int_0^1 x^2\,dx = \left[\frac{x^3}{3}\right]_0^1 = \frac{1}{3}$$
            """, mathjax=True),

            dcc.Markdown(r"""
**Exemplo 2:** Área entre $y = x^2$ e $y = \sqrt{x}$ de $0$ a $1$.

**Passo 1:** Verificar qual função é maior. Em $x = 0{,}5$: $\sqrt{0{,}5} \approx 0{,}707 > 0{,}25 = (0{,}5)^2$.
Logo $\sqrt{x} \geq x^2$ em $[0,1]$.

**Passo 2:**
$$A = \int_0^1 \left(\sqrt{x} - x^2\right)dx = \left[\frac{2}{3}x^{3/2} - \frac{x^3}{3}\right]_0^1 = \frac{2}{3} - \frac{1}{3} = \boxed{\frac{1}{3}}$$
            """, mathjax=True),

            dcc.Markdown(r"""
**Exemplo 3:** Área entre $y = x$ e $y = x^2$ de $0$ a $1$.

Em $[0,1]$: $x \geq x^2$ (pois $x - x^2 = x(1-x) \geq 0$).

$$A = \int_0^1 (x - x^2)\,dx = \left[\frac{x^2}{2} - \frac{x^3}{3}\right]_0^1 = \frac{1}{2} - \frac{1}{3} = \boxed{\frac{1}{6}}$$
            """, mathjax=True),
        ]),

        section("Gráfico Interativo: Área entre Curvas", [
            conceito(r"""
Área entre $f(x)$ e $g(x)$: $A = \int_a^b [f(x) - g(x)]\,dx$. No caso $f(x) = x^3 - 3x$,
note a diferença entre a integral com sinal e a área geométrica $\int |f|\,dx$.
            """),
            dbc.Row([
                dbc.Col([
                    html.Label("Par de funções:", style={"fontWeight": "600"}),
                    dcc.Dropdown(id="dropdown-area-func",
                        options=[
                            {"label": "y = x² vs y = √x  em [0,1]", "value": "x2_sqrtx"},
                            {"label": "y = x vs y = x²  em [0,1]", "value": "x_x2"},
                            {"label": "y = x² vs y = 2  em [0,√2]", "value": "x2_const"},
                            {"label": "y = x³−3x vs y = 0 (área com |f|)  em [−1,2]", "value": "cubica"},
                        ], value="x2_sqrtx", clearable=False),
                ], md=6),
            ]),
            dcc.Graph(id="graph-area", config=PCFG),
        ]),

        section("Aplicação Econômica: Excedente como Área entre Curvas", [
            dcc.Markdown(r"""
Em Economia, a área entre curvas tem interpretação direta como medida de **bem-estar**
(Simon & Blume, Cap. 18):

- **Excedente do Consumidor (EC):** Área entre a curva de demanda e a linha de preço.
  Representa a diferença entre o que os consumidores estão *dispostos* a pagar e o que *efetivamente* pagam.

- **Excedente do Produtor (EP):** Área entre a linha de preço e a curva de oferta.

$$EC = \int_0^{q^*} f(q)\,dq - p^* \cdot q^*$$

O excedente total (EC + EP) mede o ganho de bem-estar gerado pela troca no mercado.
Veremos isso em detalhes na página de **Aplicações Econômicas**.
            """, mathjax=True),
        ]),

        footer(),
    ])

# ═══════════════════════════════════════════
#  PÁGINA 6 — TÉCNICAS DE INTEGRAÇÃO
# ═══════════════════════════════════════════

def pg_tecnicas():
    return wrap([
        html.H3("Técnicas de Integração"),
        html.Hr(),

        section("Motivação", [
            dcc.Markdown(r"""
A tabela de primitivas imediatas cobre apenas os casos básicos. Integrais como
$\int e^{3x}\,dx$, $\int (2x+1)^5\,dx$ ou $\int x\,e^x\,dx$ exigem métodos que
transformem o integrando em uma forma conhecida.

As duas técnicas fundamentais são:
1. **Substituição** (mudança de variável), que inverte a regra da cadeia
2. **Integração por partes**, que inverte a regra do produto
            """, mathjax=True),
        ]),

        # ── SUBSTITUIÇÃO ──
        section("Método de Substituição (Mudança de Variável)", [
            dcc.Markdown(r"""
Quando o integrando contém uma composição $f(g(x))$ multiplicada pela derivada
$g'(x)$, a substituição $u = g(x)$ simplifica a integral.

Pela regra da cadeia: $[F(g(x))]' = f(g(x)) \cdot g'(x)$. Integrando ambos os lados:
            """, mathjax=True),

            eq_box(r"""
$$\int f(g(x))\,g'(x)\,dx = F(g(x)) + C$$

Na prática, fazemos $u = g(x)$, $du = g'(x)\,dx$ e escrevemos:
$$\int f(g(x))\,g'(x)\,dx = \int f(u)\,du$$
            """),

            mario_code("Demonstração: Fórmula de substituição", r"""
**Partindo da regra da cadeia:**

Sabemos que se $F$ é primitiva de $f$ (ou seja, $F' = f$), então:
$$\frac{d}{dx}\big[F(g(x))\big] = F'(g(x)) \cdot g'(x) = f(g(x)) \cdot g'(x)$$

Isso significa que $F(g(x))$ é uma primitiva de $f(g(x)) \cdot g'(x)$.

Portanto:
$$\int f(g(x)) \cdot g'(x)\,dx = F(g(x)) + C$$

Se chamarmos $u = g(x)$, então $du = g'(x)\,dx$, e a integral se torna:
$$\int f(u)\,du = F(u) + C = F(g(x)) + C \qquad \blacksquare$$

**Em palavras:** a substituição "desfaz" a regra da cadeia.
            """),

            dcc.Markdown(r"""
**Estratégia prática:**
1. Identifique uma "função interna" $g(x)$ no integrando
2. Verifique se $g'(x)$ aparece (a menos de uma constante) como fator
3. Faça $u = g(x)$, $du = g'(x)\,dx$
4. Reescreva tudo em termos de $u$
5. Integre em $u$
6. Substitua de volta $u = g(x)$
            """, mathjax=True),

            mario_code("Exemplo 1: ∫ e^(3x) dx", r"""
**Passo 1:** Identificar $u = 3x$, logo $du = 3\,dx$, ou seja $dx = \frac{du}{3}$.

**Passo 2:** Substituir:
$$\int e^{3x}\,dx = \int e^u \cdot \frac{du}{3} = \frac{1}{3}\int e^u\,du$$

**Passo 3:** Integrar e voltar à variável original:
$$= \frac{1}{3}e^u + C = \boxed{\frac{1}{3}e^{3x} + C}$$

**Verificação:** $\left(\frac{1}{3}e^{3x}\right)' = \frac{1}{3} \cdot 3e^{3x} = e^{3x}$ ✓
            """),

            mario_code("Exemplo 2: ∫ (2x+1)³ dx", r"""
**Passo 1:** $u = 2x + 1$, $du = 2\,dx \implies dx = \frac{du}{2}$.

**Passo 2:**
$$\int (2x+1)^3\,dx = \frac{1}{2}\int u^3\,du = \frac{1}{2}\cdot\frac{u^4}{4} = \frac{u^4}{8}$$

**Passo 3:** Voltar:
$$= \boxed{\frac{(2x+1)^4}{8} + C}$$

**Verificação:** $\left(\frac{(2x+1)^4}{8}\right)' = \frac{4(2x+1)^3 \cdot 2}{8} = (2x+1)^3$ ✓
            """),

            mario_code("Exemplo 3: ∫ x/(1+x²) dx", r"""
**Passo 1:** $u = 1 + x^2$, $du = 2x\,dx \implies x\,dx = \frac{du}{2}$.

**Passo 2:**
$$\int \frac{x}{1+x^2}\,dx = \frac{1}{2}\int \frac{du}{u} = \frac{1}{2}\ln|u|$$

**Passo 3:**
$$= \boxed{\frac{1}{2}\ln(1+x^2) + C}$$

(Note que $1+x^2 > 0$ sempre, então $|u| = u$.)

**Verificação:** $\left(\frac{1}{2}\ln(1+x^2)\right)' = \frac{1}{2}\cdot\frac{2x}{1+x^2} = \frac{x}{1+x^2}$ ✓
            """),

            mario_code("Exemplo 4: ∫ x·√(x²+1) dx", r"""
**Passo 1:** $u = x^2 + 1$, $du = 2x\,dx \implies x\,dx = \frac{du}{2}$.

**Passo 2:**
$$\int x\sqrt{x^2+1}\,dx = \frac{1}{2}\int \sqrt{u}\,du = \frac{1}{2}\cdot\frac{u^{3/2}}{3/2} = \frac{1}{3}u^{3/2}$$

**Passo 3:**
$$= \boxed{\frac{1}{3}(x^2+1)^{3/2} + C}$$

**Verificação:** $\left(\frac{1}{3}(x^2+1)^{3/2}\right)' = \frac{1}{3}\cdot\frac{3}{2}(x^2+1)^{1/2}\cdot 2x = x\sqrt{x^2+1}$ ✓
            """),
        ]),

        section("Substituição em Integrais Definidas", [
            eq_box(r"""
Se $u = g(x)$, com $g(a) = \alpha$ e $g(b) = \beta$:
$$\int_a^b f(g(x))\,g'(x)\,dx = \int_\alpha^\beta f(u)\,du$$
**Atenção:** os limites de integração mudam junto com a variável!
            """),
            dcc.Markdown(r"""
**Exemplo:** $\displaystyle\int_0^1 (x-1)^{10}\,dx$.

$u = x - 1$: quando $x=0 \to u=-1$; quando $x=1 \to u=0$. E $du = dx$.

$$\int_0^1 (x-1)^{10}\,dx = \int_{-1}^0 u^{10}\,du = \left[\frac{u^{11}}{11}\right]_{-1}^0 = 0 - \frac{(-1)^{11}}{11} = \frac{1}{11}$$
            """, mathjax=True),
        ]),

        html.Hr(),

        # ── INTEGRAÇÃO POR PARTES ──
        section("Integração por Partes", [
            dcc.Markdown(r"""
Quando o integrando é um produto de duas funções e a substituição não se aplica,
utilizamos a integração por partes, que inverte a regra do produto para derivadas.
            """, mathjax=True),

            eq_box(r"""
$$\int u\,dv = u\cdot v - \int v\,du$$

ou equivalentemente: $\displaystyle\int f(x)\,g'(x)\,dx = f(x)\,g(x) - \int f'(x)\,g(x)\,dx$
            """),

            mario_code("Demonstração: Fórmula de integração por partes", r"""
Partindo da **regra do produto** para derivadas:
$$(f \cdot g)' = f' \cdot g + f \cdot g'$$

Rearranjando:
$$f \cdot g' = (f \cdot g)' - f' \cdot g$$

Integrando ambos os lados:
$$\int f(x) \cdot g'(x)\,dx = \int (f \cdot g)'\,dx - \int f'(x) \cdot g(x)\,dx$$

Como $\int (f \cdot g)'\,dx = f(x) \cdot g(x)$:
$$\int f(x) \cdot g'(x)\,dx = f(x) \cdot g(x) - \int f'(x) \cdot g(x)\,dx \qquad \blacksquare$$

Fazendo $u = f(x)$ e $v = g(x)$:
$$\int u\,dv = uv - \int v\,du$$
            """),

            dcc.Markdown(r"""
**Regra LIATE para escolha de $u$** (em ordem de prioridade):

| Prioridade | Tipo | Exemplos |
|:---:|:---|:---|
| 1.º | **L**ogarítmica | $\ln x$, $\log x$ |
| 2.º | **I**nversa (funções inversas) | $\sqrt{x}$, $x^{1/n}$ |
| 3.º | **A**lgébrica (polinomial) | $x$, $x^2$, $x^3$ |
| 4.º | **E**xponencial | $e^x$, $2^x$ |

**Dica:** Escolha $u$ como a função que fica **mais simples ao derivar** e $dv$ como
o restante (que você saiba integrar).
            """, mathjax=True),

            mario_code("Exemplo 1: ∫ x·eˣ dx", r"""
**Escolha (LIATE):** $u = x$ (algébrica, simplifica ao derivar), $dv = e^x\,dx$.

**Passo 1:** $du = dx$, $v = e^x$.

**Passo 2:** Aplicar a fórmula $\int u\,dv = uv - \int v\,du$:
$$\int x\,e^x\,dx = x\,e^x - \int e^x\,dx$$

**Passo 3:** A integral restante é imediata:
$$= x\,e^x - e^x + C = \boxed{e^x(x-1) + C}$$

**Verificação:** $[e^x(x-1)]' = e^x(x-1) + e^x \cdot 1 = e^x \cdot x$ ✓
            """),

            mario_code("Exemplo 2: ∫ x²·eˣ dx (partes dupla)", r"""
Aqui precisamos aplicar partes **duas vezes**:

**1.ª aplicação:** $u = x^2$, $dv = e^x\,dx \implies du = 2x\,dx$, $v = e^x$.

$$\int x^2 e^x\,dx = x^2 e^x - 2\int x\,e^x\,dx$$

**2.ª aplicação** (na integral restante): $u = x$, $dv = e^x\,dx$:

$$\int x\,e^x\,dx = x\,e^x - e^x \quad \text{(do exemplo anterior)}$$

**Combinando:**
$$\int x^2 e^x\,dx = x^2 e^x - 2(x\,e^x - e^x) + C = \boxed{e^x(x^2 - 2x + 2) + C}$$
            """),

            mario_code("Exemplo 3: ∫ ln(x) dx", r"""
**Escolha (LIATE):** $u = \ln x$ (logarítmica — prioridade máxima), $dv = dx$.

**Passo 1:** $du = \dfrac{1}{x}\,dx$, $v = x$.

**Passo 2:**
$$\int \ln x\,dx = x\ln x - \int x \cdot \frac{1}{x}\,dx = x\ln x - \int 1\,dx$$

**Passo 3:**
$$= \boxed{x\ln x - x + C}$$

**Verificação:** $(x\ln x - x)' = \ln x + x \cdot \frac{1}{x} - 1 = \ln x$ ✓
            """),

            mario_code("Exemplo 4: ∫ x·ln(x) dx", r"""
**Escolha (LIATE):** $u = \ln x$, $dv = x\,dx$.

**Passo 1:** $du = \dfrac{1}{x}\,dx$, $v = \dfrac{x^2}{2}$.

**Passo 2:**
$$\int x\ln x\,dx = \frac{x^2}{2}\ln x - \int \frac{x^2}{2}\cdot\frac{1}{x}\,dx = \frac{x^2}{2}\ln x - \frac{1}{2}\int x\,dx$$

**Passo 3:**
$$= \frac{x^2}{2}\ln x - \frac{1}{2}\cdot\frac{x^2}{2} + C = \boxed{\frac{x^2}{2}\ln x - \frac{x^2}{4} + C}$$

**Verificação:** $\left(\frac{x^2}{2}\ln x - \frac{x^2}{4}\right)' = x\ln x + \frac{x}{2} - \frac{x}{2} = x\ln x$ ✓
            """),
        ]),

        section("Gráfico Interativo: Visualização da Substituição", [
            conceito(r"""
A substituição $u = g(x)$ simplifica o integrando. Painel esquerdo: função original em $x$.
Painel direito: função transformada em $u$. A área sob ambas as curvas é a mesma.
            """),
            dbc.Row([
                dbc.Col([
                    html.Label("Exemplo:", style={"fontWeight": "600"}),
                    dcc.Dropdown(id="dropdown-subst-ex",
                        options=[
                            {"label": "∫ e^(3x) dx  →  u = 3x", "value": "e3x"},
                            {"label": "∫ x/(1+x²) dx  →  u = 1+x²", "value": "x_1x2"},
                            {"label": "∫ x·e^(x²) dx  →  u = x²", "value": "xex2"},
                        ], value="e3x", clearable=False),
                ], md=6),
            ]),
            dcc.Graph(id="graph-substituicao", config=PCFG),
        ]),

        footer(),
    ])

# ═══════════════════════════════════════════
#  PÁGINA 7 — FRAÇÕES PARCIAIS
# ═══════════════════════════════════════════

def pg_fracoes_parciais():
    return wrap([
        html.H3("Integração por Frações Parciais"),
        html.Hr(),

        section("Ideia Geral", [
            dcc.Markdown(r"""
Para integrar uma **função racional** $\frac{P(x)}{Q(x)}$ (razão de dois polinômios),
a estratégia consiste em decompor a fração em parcelas mais simples, cada uma integrável
diretamente.

Por exemplo, $\frac{x+3}{x^2-3x+2} = \frac{-4}{x-1} + \frac{5}{x-2}$, e cada
parcela integra como $\int \frac{A}{x-a}\,dx = A\ln|x-a| + C$.
            """, mathjax=True),
        ]),

        section("Decomposição com Dois Fatores Lineares Distintos", [
            conceito(r"""
**Teorema:** Sejam $\alpha \neq \beta$ reais. Para quaisquer $m, n$ reais, existem constantes $A$ e $B$ tais que:
$$\frac{mx + n}{(x - \alpha)(x - \beta)} = \frac{A}{x - \alpha} + \frac{B}{x - \beta}$$
            """),
            mario_code("Demonstração: existência de A e B", r"""
Multiplicando ambos os lados por $(x-\alpha)(x-\beta)$:
$$mx + n = A(x - \beta) + B(x - \alpha)$$

Essa igualdade deve valer para **todo** $x$. Escolhendo valores estratégicos:

- **$x = \alpha$:** $m\alpha + n = A(\alpha - \beta) \implies A = \dfrac{m\alpha + n}{\alpha - \beta}$

- **$x = \beta$:** $m\beta + n = B(\beta - \alpha) \implies B = \dfrac{m\beta + n}{\beta - \alpha}$

Como $\alpha \neq \beta$, os denominadores são não-nulos e $A, B$ estão bem definidos. $\blacksquare$
            """),

            dcc.Markdown(r"""
**Resultado:** Se o grau do numerador $P(x)$ for estritamente menor que o grau do denominador:
$$\int \frac{P(x)}{(x-\alpha)(x-\beta)}\,dx = A\ln|x - \alpha| + B\ln|x - \beta| + C$$

Se grau$(P) \geq$ grau do denominador, faz-se a **divisão polinomial** primeiro:
$$\frac{P(x)}{Q(x)} = \underbrace{S(x)}_{\text{quociente}} + \underbrace{\frac{R(x)}{Q(x)}}_{\text{resto/den}}$$
            """, mathjax=True),

            mario_code("Exemplo 1: ∫ (x+3)/(x²-3x+2) dx", r"""
**Passo 1:** Fatorar o denominador: $x^2 - 3x + 2 = (x-1)(x-2)$.

**Passo 2:** Decompor:
$$\frac{x+3}{(x-1)(x-2)} = \frac{A}{x-1} + \frac{B}{x-2}$$

Multiplicando por $(x-1)(x-2)$:
$$x + 3 = A(x-2) + B(x-1)$$

**Passo 3:** Determinar $A$ e $B$ usando valores estratégicos:
- $x = 1$: $1 + 3 = A(1-2) \implies 4 = -A \implies A = -4$
- $x = 2$: $2 + 3 = B(2-1) \implies 5 = B \implies B = 5$

**Passo 4:** Integrar:
$$\int \frac{x+3}{(x-1)(x-2)}\,dx = \int\frac{-4}{x-1}\,dx + \int\frac{5}{x-2}\,dx = \boxed{-4\ln|x-1| + 5\ln|x-2| + C}$$
            """),

            mario_code("Exemplo 2: ∫ (x²+2)/(x²-3x+2) dx  (grau ≥ denominador)", r"""
**Passo 1:** Como grau(num) = grau(den) = 2, fazemos a **divisão polinomial**:
$$\frac{x^2 + 2}{x^2 - 3x + 2} = 1 + \frac{3x}{x^2 - 3x + 2} = 1 + \frac{3x}{(x-1)(x-2)}$$

(Pois $x^2 + 2 = 1 \cdot (x^2 - 3x + 2) + (3x)$)

**Passo 2:** Decompor o resto:
$$\frac{3x}{(x-1)(x-2)} = \frac{A}{x-1} + \frac{B}{x-2}$$

$3x = A(x-2) + B(x-1)$
- $x = 1$: $3 = -A \implies A = -3$
- $x = 2$: $6 = B \implies B = 6$

**Passo 3:** Integrar:
$$\int \frac{x^2+2}{(x-1)(x-2)}\,dx = \int 1\,dx + \int\frac{-3}{x-1}\,dx + \int\frac{6}{x-2}\,dx$$

$$= \boxed{x - 3\ln|x-1| + 6\ln|x-2| + C}$$
            """),
        ]),

        section("Decomposição com Três Fatores", [
            conceito(r"""
**Teorema:** Sejam $\alpha, \beta, \gamma$ reais distintos. Existem $A, B, C$ tais que:
$$\frac{mx^2 + nx + p}{(x-\alpha)(x-\beta)(x-\gamma)} = \frac{A}{x-\alpha} + \frac{B}{x-\beta} + \frac{C}{x-\gamma}$$
            """),
            dcc.Markdown(r"""
**Caso com fator repetido:** Se um fator aparece ao quadrado, a decomposição muda:
$$\frac{mx^2 + nx + p}{(x-\alpha)(x-\beta)^2} = \frac{A}{x-\alpha} + \frac{B}{x-\beta} + \frac{C}{(x-\beta)^2}$$

Note que o fator $(x-\beta)^2$ gera **dois** termos: um com $(x-\beta)$ e outro com $(x-\beta)^2$.
            """, mathjax=True),

            mario_code("Exemplo 3: ∫ (x⁴+2x+1)/(x³-x²-2x) dx", r"""
**Passo 1:** Fatorar: $x^3 - x^2 - 2x = x(x^2 - x - 2) = x(x-2)(x+1)$.

**Passo 2:** Grau(num)=4 > grau(den)=3, então dividimos primeiro:

Fazendo a divisão de $x^4 + 2x + 1$ por $x^3 - x^2 - 2x$:
$$\frac{x^4 + 2x + 1}{x^3 - x^2 - 2x} = (x + 1) + \frac{3x^2 + 4x + 1}{x(x-2)(x+1)}$$

**Passo 3:** Decompor o resto:
$$\frac{3x^2 + 4x + 1}{x(x-2)(x+1)} = \frac{A}{x} + \frac{B}{x-2} + \frac{C}{x+1}$$

$3x^2 + 4x + 1 = A(x-2)(x+1) + Bx(x+1) + Cx(x-2)$

- $x = 0$: $1 = A(-2)(1) \implies A = -\frac{1}{2}$
- $x = 2$: $12+8+1 = B(2)(3) \implies 21 = 6B \implies B = \frac{7}{2}$
- $x = -1$: $3-4+1 = C(-1)(-3) \implies 0 = 3C \implies C = 0$

**Passo 4:**
$$\int \frac{x^4+2x+1}{x^3-x^2-2x}\,dx = \frac{x^2}{2} + x - \frac{1}{2}\ln|x| + \frac{7}{2}\ln|x-2| + K$$
            """),
        ]),

        section("Gráfico Interativo: Decomposição Visual", [
            conceito(r"""
$\frac{mx+n}{(x-\alpha)(x-\beta)} = \frac{A}{x-\alpha} + \frac{B}{x-\beta}$. A curva original (vermelha)
é a soma das frações parciais (tracejadas). Varie $m, n, \alpha, \beta$ para explorar a decomposição.
            """),
            dbc.Row([
                dbc.Col([
                    html.Label("m (coef. de x no numerador):", style={"fontWeight": "600"}),
                    dcc.Slider(id="slider-fp-m", min=-3, max=3, step=1, value=1,
                        marks={i: str(i) for i in range(-3, 4)},
                        tooltip={"placement": "bottom"}),
                ], md=3),
                dbc.Col([
                    html.Label("n (termo independente no num.):", style={"fontWeight": "600"}),
                    dcc.Slider(id="slider-fp-n", min=-5, max=5, step=1, value=3,
                        marks={i: str(i) for i in range(-5, 6, 2)},
                        tooltip={"placement": "bottom"}),
                ], md=3),
                dbc.Col([
                    html.Label("α (raiz 1 do den.):", style={"fontWeight": "600"}),
                    dcc.Slider(id="slider-fp-alpha", min=-3, max=0, step=1, value=-1,
                        marks={i: str(i) for i in range(-3, 1)},
                        tooltip={"placement": "bottom"}),
                ], md=3),
                dbc.Col([
                    html.Label("β (raiz 2 do den.):", style={"fontWeight": "600"}),
                    dcc.Slider(id="slider-fp-beta", min=1, max=4, step=1, value=2,
                        marks={i: str(i) for i in range(1, 5)},
                        tooltip={"placement": "bottom"}),
                ], md=3),
            ]),
            dcc.Graph(id="graph-fracoes", config=PCFG),
        ]),

        footer(),
    ])

# ═══════════════════════════════════════════
#  PÁGINA 8 — APLICAÇÕES ECONÔMICAS
# ═══════════════════════════════════════════

def pg_aplicacoes():
    return wrap([
        html.H3("Aplicações Econômicas da Integral"),
        html.Hr(),

        # ── VALOR PRESENTE E TEMPO ÓTIMO ──
        section("Valor Presente e Tempo Ótimo de Venda", [
            dcc.Markdown(r"""
Suponha que você possua um ativo (imóvel, terra, empresa) cujo valor de mercado
será $V(t)$ daqui a $t$ anos. Se a taxa de juros contínua $r$ é constante,
o **valor presente** desse ativo é:

$$VP(t) = V(t)\,e^{-rt}$$

Ou seja, $VP(t)$ é o quanto $V(t)$ "vale hoje", descontado pela taxa de juros.

**Pergunta econômica:** Quando vender para maximizar o valor presente?
            """, mathjax=True),

            eq_box(r"""
**Condição de otimalidade:** $\dfrac{dVP}{dt} = 0$ leva a:
$$V'(t)\,e^{-rt} - r\,V(t)\,e^{-rt} = 0 \implies \frac{V'(t)}{V(t)} = r$$

**Interpretação:** Venda quando a **taxa de valorização percentual** do ativo igualar a taxa de juros.
Se o ativo valoriza mais rápido que $r$, vale esperar; se valoriza mais devagar, venda agora.
            """),

            mario_code("Demonstração: derivação da condição V'(t)/V(t) = r", r"""
**Passo 1:** $VP(t) = V(t) \cdot e^{-rt}$. Derivando pelo produto:
$$VP'(t) = V'(t) \cdot e^{-rt} + V(t) \cdot (-r) \cdot e^{-rt}$$

**Passo 2:** Igualando a zero:
$$V'(t)\,e^{-rt} - r\,V(t)\,e^{-rt} = 0$$

**Passo 3:** Como $e^{-rt} > 0$ sempre, podemos dividir por $e^{-rt}$:
$$V'(t) - r\,V(t) = 0 \implies V'(t) = r\,V(t)$$

**Passo 4:** Dividindo por $V(t) > 0$:
$$\frac{V'(t)}{V(t)} = r \qquad \blacksquare$$
            """),

            mario_code("Exemplo numérico: V(t) = 10.000·e^(√t), r = 6%", r"""
**Passo 1:** Calcular $V'(t)/V(t)$:
$$V(t) = 10000\,e^{\sqrt{t}} \implies V'(t) = 10000\,e^{\sqrt{t}} \cdot \frac{1}{2\sqrt{t}}$$

$$\frac{V'(t)}{V(t)} = \frac{1}{2\sqrt{t}}$$

**Passo 2:** Igualar a $r = 0{,}06$:
$$\frac{1}{2\sqrt{t^*}} = 0{,}06 \implies \sqrt{t^*} = \frac{1}{0{,}12} \approx 8{,}33$$

$$\boxed{t^* \approx 69{,}4 \text{ anos}}$$

**Interpretação:** Nos primeiros anos, o ativo valoriza muito rápido ($V'/V$ alto),
então vale a pena esperar. Com o tempo, a valorização desacelera.
No instante $t^* \approx 69$ anos, a valorização cai ao nível da taxa de juros.
            """),
        ]),

        section("Gráfico Interativo: Tempo Ótimo de Investimento", [
            conceito(r"""
Painel esquerdo: $VP(t) = V(t)\,e^{-rt}$ com o máximo marcado. Painel direito:
$V'(t)/V(t)$ vs $r$, cujo cruzamento determina $t^*$. Quanto maior $r$, mais cedo convém vender.
            """),
            dbc.Row([
                dbc.Col([
                    html.Label("Taxa de juros r (%):", style={"fontWeight": "600"}),
                    dcc.Slider(id="slider-tempo-r", min=1, max=15, step=0.5, value=6,
                        marks={i: f"{i}%" for i in range(1, 16, 2)},
                        tooltip={"placement": "bottom"}),
                ], md=6),
                dbc.Col([
                    html.Label("Função V(t):", style={"fontWeight": "600"}),
                    dcc.Dropdown(id="dropdown-tempo-vt",
                        options=[
                            {"label": "V(t) = 10000·e^(√t)", "value": "sqrt"},
                            {"label": "V(t) = 10000·e^(t/10)", "value": "linear"},
                            {"label": "V(t) = 10000·ln(1+t)", "value": "log"},
                        ], value="sqrt", clearable=False),
                ], md=6),
            ]),
            dcc.Graph(id="graph-tempo-otimo", config=PCFG),
        ]),

        # ── EXCEDENTE DO CONSUMIDOR ──
        section("Excedente do Consumidor", [
            dcc.Markdown(r"""
Seja $p = f(q)$ a **função demanda inversa**, que relaciona o preço à quantidade.

Imagine que o bem é vendido em pequenos lotes, com preços decrescentes. Os primeiros
consumidores (que valorizam mais o produto) pagam preços maiores. O gasto total seria:
$$\text{Disposição Total a Pagar} = \sum_{i=1}^{n} f(q_i)(q_i - q_{i-1}) \approx \int_0^{q^*} f(q)\,dq$$

Porém, na prática (sem discriminação de preços), todos pagam $p^* = f(q^*)$.
A diferença é o **excedente do consumidor** — o "bônus" que os consumidores recebem:
            """, mathjax=True),

            eq_box(r"""
$$EC = \int_0^{q^*} f(q)\,dq - p^* \cdot q^* = \int_0^{q^*} \big[f(q) - p^*\big]\,dq$$

**Interpretação:** EC é a área entre a curva de demanda e a linha de preço $p^*$.
            """),

            mario_code("Exemplo: demanda linear p = 100 − 2q, q* = 30", r"""
**Passo 1:** Preço de equilíbrio: $p^* = 100 - 2(30) = 40$.

**Passo 2:** Disposição total a pagar:
$$DTP = \int_0^{30} (100 - 2q)\,dq = \left[100q - q^2\right]_0^{30} = 3000 - 900 = 2100$$

**Passo 3:** Despesa efetiva: $p^* \cdot q^* = 40 \times 30 = 1200$.

**Passo 4:** $$\boxed{EC = 2100 - 1200 = 900 \text{ u.m.}}$$

**Interpretação:** Os consumidores, coletivamente, estariam dispostos a pagar R$ 2.100,
mas pagam apenas R$ 1.200. O "ganho" coletivo é R$ 900.

**Atalho geométrico:** Como a demanda é linear, o EC é a área de um triângulo:
$$EC = \frac{1}{2} \cdot \text{base} \cdot \text{altura} = \frac{1}{2} \cdot 30 \cdot (100 - 40) = \frac{1}{2} \cdot 30 \cdot 60 = 900$$
            """),
        ]),

        section("Gráfico Interativo: Excedente do Consumidor", [
            conceito(r"""
$EC = \int_0^{q^*} f(q)\,dq - p^*q^*$. Área sombreada: excedente do consumidor.
Curva vermelha: demanda inversa. Linha tracejada: preço $p^*$.
            """),
            dbc.Row([
                dbc.Col([
                    html.Label("Quantidade q*:", style={"fontWeight": "600"}),
                    dcc.Slider(id="slider-ec-q", min=5, max=45, step=5, value=30,
                        marks={i: str(i) for i in range(5, 50, 5)},
                        tooltip={"placement": "bottom"}),
                ], md=6),
                dbc.Col([
                    html.Label("Função demanda inversa:", style={"fontWeight": "600"}),
                    dcc.Dropdown(id="dropdown-ec-func",
                        options=[
                            {"label": "p = 100 − 2q  (linear)", "value": "linear"},
                            {"label": "p = 50·e^(-0.02q)  (exponencial)", "value": "exp"},
                            {"label": "p = 200/(q+2)  (hiperbólica)", "value": "hiper"},
                        ], value="linear", clearable=False),
                ], md=6),
            ]),
            dcc.Graph(id="graph-ec", config=PCFG),
        ]),

        # ── CUSTO / RECEITA ──
        section("Custo Total e Receita Total (Simon & Blume)", [
            dcc.Markdown(r"""
A integral conecta grandezas **marginais** (taxas de variação) a grandezas **totais**.
Em Economia (Simon & Blume, Cap. 17):

- **Custo marginal** $C'(q)$: custo adicional de produzir **uma unidade a mais**
- **Receita marginal** $R'(q)$: receita adicional de vender **uma unidade a mais**

A integral recupera as funções totais:
$$C(q) = \int_0^q C'(t)\,dt + C_0 \qquad\qquad R(q) = \int_0^q R'(t)\,dt$$

O **lucro** é $\Pi(q) = R(q) - C(q)$, maximizado quando $R'(q) = C'(q)$
(receita marginal = custo marginal).

A área entre as curvas $R'(q)$ e $C'(q)$ representa o lucro (ou prejuízo) acumulado:
$$\Pi(q) - \Pi(0) = \int_0^q \big[R'(t) - C'(t)\big]\,dt$$
            """, mathjax=True),

            mario_code("Demonstração: lucro máximo quando R'(q) = C'(q)", r"""
**Passo 1:** O lucro é $\Pi(q) = R(q) - C(q)$.

**Passo 2:** Condição necessária para máximo: $\Pi'(q) = 0$:
$$\Pi'(q) = R'(q) - C'(q) = 0 \implies R'(q) = C'(q)$$

**Passo 3:** Condição suficiente: $\Pi''(q) < 0$:
$$\Pi''(q) = R''(q) - C''(q) < 0$$

Isso ocorre quando a receita marginal está **decrescendo mais rápido** que o custo marginal
está crescendo, ou equivalentemente, quando a curva de $R'$ cruza a curva de $C'$ **de cima para baixo**.

**Em palavras:** enquanto a receita de uma unidade adicional supera seu custo, vale produzir mais.
No ponto ótimo, a última unidade produzida gera receita exatamente igual ao seu custo. $\blacksquare$
            """),
        ]),

        section("Gráfico Interativo: Custo e Receita Marginal", [
            conceito(r"""
Painel esquerdo: $C'(q) = aq + b$ vs $R'(q) = p$. A interseção define $q^*$ (quantidade ótima).
Painel direito: $C(q)$, $R(q)$ e $\Pi(q) = R - C$. Note que $C_0$ não afeta $q^*$, mas altera $\Pi$.
            """),
            dbc.Row([
                dbc.Col([
                    html.Label("Custo marginal: C'(q) = aq + b", style={"fontWeight": "600"}),
                    html.Label("a:", style={"fontWeight": "600", "fontSize": "14px"}),
                    dcc.Slider(id="slider-cr-a", min=0.5, max=4, step=0.5, value=2,
                        marks={i: str(i) for i in range(1, 5)},
                        tooltip={"placement": "bottom"}),
                    html.Label("b:", style={"fontWeight": "600", "fontSize": "14px"}),
                    dcc.Slider(id="slider-cr-b", min=0, max=20, step=2, value=10,
                        marks={i: str(i) for i in range(0, 22, 4)},
                        tooltip={"placement": "bottom"}),
                ], md=4),
                dbc.Col([
                    html.Label("Preço (receita marginal constante):", style={"fontWeight": "600"}),
                    dcc.Slider(id="slider-cr-p", min=10, max=80, step=5, value=50,
                        marks={i: str(i) for i in range(10, 90, 10)},
                        tooltip={"placement": "bottom"}),
                ], md=4),
                dbc.Col([
                    html.Label("Custo fixo C₀:", style={"fontWeight": "600"}),
                    dcc.Slider(id="slider-cr-c0", min=0, max=500, step=50, value=200,
                        marks={i: str(i) for i in range(0, 600, 100)},
                        tooltip={"placement": "bottom"}),
                ], md=4),
            ]),
            dcc.Graph(id="graph-custo-receita", config=PCFG),
        ]),

        footer(),
    ])

# ═══════════════════════════════════════════
#  PÁGINA 9 — EXERCÍCIOS
# ═══════════════════════════════════════════

def pg_exercicios():
    return wrap([
        html.H3("Exercícios de Fixação"),
        html.Hr(),

        dcc.Markdown(r"""
Resolva os exercícios abaixo. Clique na caixa **?** para ver a solução detalhada.
Tente resolver sozinho antes de consultar!
        """, mathjax=True),

        # ── Exercício 1 ──
        mario_question(
            "Exercício 1 — Primitivas imediatas: Calcule (a) ∫(3x² − 2x + 5) dx   (b) ∫e^(4x) dx   (c) ∫(1/x + √x) dx",
            r"""
**a)** Aplicando a regra da potência termo a termo:
$$\int(3x^2 - 2x + 5)\,dx = 3\cdot\frac{x^3}{3} - 2\cdot\frac{x^2}{2} + 5x + C = \boxed{x^3 - x^2 + 5x + C}$$

**Verificação:** $(x^3 - x^2 + 5x)' = 3x^2 - 2x + 5$ ✓

---

**b)** Usando $\int e^{\alpha x}\,dx = \frac{e^{\alpha x}}{\alpha} + C$ com $\alpha = 4$:
$$\int e^{4x}\,dx = \boxed{\frac{e^{4x}}{4} + C}$$

**Verificação:** $\left(\frac{e^{4x}}{4}\right)' = \frac{4e^{4x}}{4} = e^{4x}$ ✓

---

**c)** $\displaystyle\int\left(\frac{1}{x} + \sqrt{x}\right)dx = \int\frac{1}{x}\,dx + \int x^{1/2}\,dx$

$$= \ln|x| + \frac{x^{3/2}}{3/2} + C = \boxed{\ln|x| + \frac{2}{3}x\sqrt{x} + C}$$
            """,
        ),

        # ── Exercício 2 ──
        mario_question(
            "Exercício 2 — PVI: Uma partícula tem velocidade v(t) = 6t² − 4t + 1 e posição x(0) = 3. Encontre x(t) e calcule x(2).",
            r"""
**Passo 1:** Integrar a velocidade para obter a posição:
$$x(t) = \int v(t)\,dt = \int(6t^2 - 4t + 1)\,dt = 2t^3 - 2t^2 + t + C$$

**Passo 2:** Usar a condição inicial $x(0) = 3$:
$$2(0)^3 - 2(0)^2 + 0 + C = 3 \implies C = 3$$

$$\boxed{x(t) = 2t^3 - 2t^2 + t + 3}$$

**Passo 3:** Calcular $x(2)$:
$$x(2) = 2(8) - 2(4) + 2 + 3 = 16 - 8 + 2 + 3 = \boxed{13}$$
            """,
        ),

        # ── Exercício 3 ──
        mario_question(
            "Exercício 3 — Integrais definidas: Calcule (a) ∫₀³(x²+1) dx   (b) ∫₁⁴(1/√x) dx   (c) ∫₀¹ e^(−2x) dx",
            r"""
**a)** $\displaystyle\int_0^3 (x^2 + 1)\,dx = \left[\frac{x^3}{3} + x\right]_0^3 = \left(\frac{27}{3} + 3\right) - 0 = 9 + 3 = \boxed{12}$

---

**b)** $\displaystyle\int_1^4 \frac{1}{\sqrt{x}}\,dx = \int_1^4 x^{-1/2}\,dx = \left[\frac{x^{1/2}}{1/2}\right]_1^4 = \left[2\sqrt{x}\right]_1^4 = 2(2) - 2(1) = \boxed{2}$

---

**c)** Primitiva de $e^{-2x}$: $F(x) = \frac{e^{-2x}}{-2} = -\frac{1}{2}e^{-2x}$.

$\displaystyle\int_0^1 e^{-2x}\,dx = \left[-\frac{1}{2}e^{-2x}\right]_0^1 = -\frac{1}{2}e^{-2} + \frac{1}{2} = \frac{1}{2}\left(1 - e^{-2}\right) \approx \boxed{0{,}432}$
            """,
        ),

        # ── Exercício 4 ──
        mario_question(
            "Exercício 4 — Área: Calcule a área da região entre y = x² e y = 2x no intervalo [0, 2].",
            r"""
**Passo 1:** Encontrar interseções: $x^2 = 2x \implies x(x - 2) = 0 \implies x = 0$ ou $x = 2$.

**Passo 2:** Verificar qual função é maior em $(0, 2)$. Em $x = 1$: $2(1) = 2 > 1 = 1^2$. Logo $2x \geq x^2$ no intervalo.

**Passo 3:** Calcular a área:
$$A = \int_0^2 (2x - x^2)\,dx = \left[x^2 - \frac{x^3}{3}\right]_0^2 = 4 - \frac{8}{3} = \frac{12 - 8}{3} = \boxed{\frac{4}{3} \approx 1{,}333}$$
            """,
        ),

        # ── Exercício 5 ──
        mario_question(
            "Exercício 5 — Substituição: Calcule (a) ∫x·√(x²+1) dx   (b) ∫x²·e^(x³) dx   (c) ∫(2x+1)/(x²+x+3) dx",
            r"""
**a)** $u = x^2 + 1$, $du = 2x\,dx \implies x\,dx = \frac{du}{2}$:
$$\int x\sqrt{x^2+1}\,dx = \frac{1}{2}\int \sqrt{u}\,du = \frac{1}{2}\cdot\frac{2}{3}u^{3/2} = \boxed{\frac{1}{3}(x^2+1)^{3/2} + C}$$

**Verificação:** $\left(\frac{1}{3}(x^2+1)^{3/2}\right)' = \frac{1}{3}\cdot\frac{3}{2}(x^2+1)^{1/2}\cdot 2x = x\sqrt{x^2+1}$ ✓

---

**b)** $u = x^3$, $du = 3x^2\,dx \implies x^2\,dx = \frac{du}{3}$:
$$\int x^2 e^{x^3}\,dx = \frac{1}{3}\int e^u\,du = \boxed{\frac{1}{3}e^{x^3} + C}$$

---

**c)** $u = x^2 + x + 3$, $du = (2x+1)\,dx$:
$$\int \frac{2x+1}{x^2+x+3}\,dx = \int \frac{du}{u} = \ln|u| + C = \boxed{\ln(x^2 + x + 3) + C}$$

($x^2 + x + 3 > 0$ sempre, pois $\Delta = 1 - 12 < 0$ e coef. líder positivo.)
            """,
        ),

        # ── Exercício 6 ──
        mario_question(
            "Exercício 6 — Integração por partes: Calcule (a) ∫x·eˣ dx   (b) ∫x·ln(x) dx   (c) ∫x²·eˣ dx",
            r"""
**a)** $u = x$, $dv = e^x\,dx \implies du = dx$, $v = e^x$:
$$\int xe^x\,dx = xe^x - \int e^x\,dx = xe^x - e^x + C = \boxed{e^x(x-1) + C}$$

---

**b)** $u = \ln x$ (LIATE: log tem prioridade), $dv = x\,dx \implies du = \frac{1}{x}\,dx$, $v = \frac{x^2}{2}$:
$$\int x\ln x\,dx = \frac{x^2}{2}\ln x - \int \frac{x^2}{2}\cdot\frac{1}{x}\,dx = \frac{x^2}{2}\ln x - \frac{1}{2}\int x\,dx$$
$$= \boxed{\frac{x^2}{2}\ln x - \frac{x^2}{4} + C}$$

---

**c)** Duas aplicações de partes:

1.ª: $u = x^2$, $dv = e^x\,dx$:
$$\int x^2 e^x\,dx = x^2 e^x - 2\int x e^x\,dx$$

2.ª (resultado do item a):
$$\int x e^x\,dx = e^x(x-1)$$

Combinando:
$$\int x^2 e^x\,dx = x^2 e^x - 2e^x(x-1) = \boxed{e^x(x^2 - 2x + 2) + C}$$
            """,
        ),

        # ── Exercício 7 ──
        mario_question(
            "Exercício 7 — Frações parciais: Calcule (a) ∫(3x+1)/((x−1)(x+2)) dx   (b) ∫(x²+1)/(x²−4) dx",
            r"""
**a)** Decompor:
$$\frac{3x+1}{(x-1)(x+2)} = \frac{A}{x-1} + \frac{B}{x+2}$$

$3x + 1 = A(x+2) + B(x-1)$
- $x = 1$: $4 = 3A \implies A = \frac{4}{3}$
- $x = -2$: $-5 = -3B \implies B = \frac{5}{3}$

$$\boxed{\int \frac{3x+1}{(x-1)(x+2)}\,dx = \frac{4}{3}\ln|x-1| + \frac{5}{3}\ln|x+2| + C}$$

---

**b)** Grau(num) = grau(den) = 2, então dividimos:
$$\frac{x^2 + 1}{x^2 - 4} = 1 + \frac{5}{x^2 - 4} = 1 + \frac{5}{(x-2)(x+2)}$$

Decompor: $\frac{5}{(x-2)(x+2)} = \frac{A}{x-2} + \frac{B}{x+2}$

$5 = A(x+2) + B(x-2)$
- $x = 2$: $5 = 4A \implies A = \frac{5}{4}$
- $x = -2$: $5 = -4B \implies B = -\frac{5}{4}$

$$\boxed{\int \frac{x^2+1}{x^2-4}\,dx = x + \frac{5}{4}\ln|x-2| - \frac{5}{4}\ln|x+2| + C}$$
            """,
        ),

        # ── Exercício 8 ──
        mario_question(
            "Exercício 8 — V/F Conceitual: Julgue as afirmações (Verdadeiro ou Falso) e justifique.",
            r"""
**(a)** "Se $F'(x) = G'(x)$ para todo $x$ em um intervalo $I$, então $F(x) = G(x)$."

**FALSO.** Pelo teorema das primitivas, $F(x) = G(x) + C$ para alguma constante $C$.
A igualdade $F = G$ só vale se $C = 0$, o que não é garantido.
Exemplo: $F(x) = x^2$ e $G(x) = x^2 + 7$ têm a mesma derivada $2x$, mas são diferentes.

---

**(b)** "Se $\int_a^b f(x)\,dx = 0$, então $f(x) = 0$ para todo $x \in [a,b]$."

**FALSO.** Contraexemplo: $\int_{-1}^{1} x\,dx = \frac{1}{2} - \frac{1}{2} = 0$, mas $f(x) = x \neq 0$.
A integral pode ser zero por cancelamento de áreas positivas e negativas.

---

**(c)** "Se $f(x) \geq 0$ em $[a,b]$, então $\int_a^b f(x)\,dx \geq 0$."

**VERDADEIRO.** Esta é a propriedade de positividade da integral de Riemann.

---

**(d)** "$\int_a^b f(x)\,dx + \int_b^c f(x)\,dx = \int_a^c f(x)\,dx$."

**VERDADEIRO.** Esta é a propriedade de aditividade em intervalos.

---

**(e)** "A integral definida $\int_a^b f(x)\,dx$ sempre representa uma área positiva."

**FALSO.** A integral definida pode ser negativa (quando $f(x) < 0$ predomina).
A **área** é $\int_a^b |f(x)|\,dx$, que é sempre $\geq 0$.
Exemplo: $\int_0^2 (x - 3)\,dx = [x^2/2 - 3x]_0^2 = 2 - 6 = -4$, mas a área é $4$.
            """,
        ),

        # ── Exercício 9 ──
        mario_question(
            "Exercício 9 — Aplicação econômica (Simon & Blume): C'(q) = 2q + 10, C(0) = 500, p(q) = 50 − q. Encontre C(q), R(q), lucro Π(q) e a quantidade q* que maximiza o lucro.",
            r"""
**Passo 1 — Custo total (via integração do custo marginal):**
$$C(q) = \int(2q + 10)\,dq = q^2 + 10q + C_0$$
Com $C(0) = 500$: $C_0 = 500$.
$$\boxed{C(q) = q^2 + 10q + 500}$$

**Passo 2 — Receita total:**
$$R(q) = p(q) \cdot q = (50 - q) \cdot q = 50q - q^2$$

Alternativamente: $R'(q) = 50 - 2q$ e $\int (50 - 2q)\,dq = 50q - q^2$.

$$\boxed{R(q) = 50q - q^2}$$

**Passo 3 — Lucro:**
$$\Pi(q) = R(q) - C(q) = (50q - q^2) - (q^2 + 10q + 500) = -2q^2 + 40q - 500$$

**Passo 4 — Maximizar (condição $R' = C'$):**
$$R'(q) = 50 - 2q, \quad C'(q) = 2q + 10$$
$$50 - 2q = 2q + 10 \implies 40 = 4q \implies \boxed{q^* = 10}$$

**Verificação:** $\Pi''(q) = -4 < 0$ (máximo confirmado).

**Lucro máximo:**
$$\Pi(10) = -2(100) + 40(10) - 500 = -200 + 400 - 500 = \boxed{-300}$$

**Interpretação:** Com estes parâmetros, a firma tem **prejuízo** de 300 u.m. mesmo na quantidade ótima.
O custo fixo ($C_0 = 500$) é muito elevado. Para ter lucro positivo, seria necessário $C_0 < 200$.
A decisão de produzir $q^* = 10$ **minimiza o prejuízo** (o melhor resultado possível dado o custo fixo).
            """,
        ),

        # ── Exercício 10 ──
        mario_question(
            "Exercício 10 — Análise integrada: Dada f(x) = x³ − 3x, (a) encontre a primitiva F(x), (b) calcule ∫₋₁² f(x) dx, (c) calcule a área entre f e o eixo x em [−1, 2], (d) interprete a diferença entre (b) e (c).",
            r"""
**a)** Primitiva:
$$F(x) = \int(x^3 - 3x)\,dx = \frac{x^4}{4} - \frac{3x^2}{2} + C$$

---

**b)** Integral definida:
$$\int_{-1}^2 (x^3 - 3x)\,dx = \left[\frac{x^4}{4} - \frac{3x^2}{2}\right]_{-1}^2$$

$$= \left(\frac{16}{4} - \frac{12}{2}\right) - \left(\frac{1}{4} - \frac{3}{2}\right) = (4 - 6) - \left(\frac{1}{4} - \frac{6}{4}\right) = -2 - (-\frac{5}{4}) = -2 + \frac{5}{4} = \boxed{-\frac{3}{4}}$$

---

**c)** Área (usando $|f|$): Raízes de $f$: $x^3 - 3x = x(x^2-3) = 0 \implies x = 0, \pm\sqrt{3}$.

Em $[-1, 0]$: testando $x = -0{,}5$: $f(-0{,}5) = -0{,}125 + 1{,}5 = 1{,}375 > 0$ → $f \geq 0$.

Em $[0, \sqrt{3}]$: testando $x = 1$: $f(1) = 1 - 3 = -2 < 0$ → $f \leq 0$.

Em $[\sqrt{3}, 2]$: testando $x = 2$: $f(2) = 8 - 6 = 2 > 0$ → $f \geq 0$.

$$A = \int_{-1}^0 f(x)\,dx + \left|\int_0^{\sqrt{3}} f(x)\,dx\right| + \int_{\sqrt{3}}^2 f(x)\,dx$$

$\displaystyle\int_{-1}^0 f\,dx = 0 - \left(\frac{1}{4} - \frac{3}{2}\right) = \frac{5}{4}$

$\displaystyle\int_0^{\sqrt{3}} f\,dx = \frac{9}{4} - \frac{9}{2} = -\frac{9}{4}$ (negativo, $|{-9/4}| = 9/4$)

$\displaystyle\int_{\sqrt{3}}^2 f\,dx = (4-6) - (\frac{9}{4}-\frac{9}{2}) = -2 + \frac{9}{4} = \frac{1}{4}$

$$A = \frac{5}{4} + \frac{9}{4} + \frac{1}{4} = \boxed{\frac{15}{4} = 3{,}75}$$

---

**d)** A integral definida $(-3/4)$ é o **balanço líquido**: regiões abaixo do eixo contribuem negativamente.
A área geométrica $(15/4)$ é sempre positiva, pois usamos $|f(x)|$.

A diferença ilustra que **integral $\neq$ área** quando $f$ muda de sinal.
A integral mede o "saldo líquido"; a área mede o "total absoluto".
            """,
        ),

        footer(),
    ])

# ═══════════════════════════════════════════
#  LAYOUT & ROTEAMENTO
# ═══════════════════════════════════════════

app.layout = html.Div([
    dcc.Location(id="url"),
    navbar(),
    html.Div(id="page-content"),
])

@callback(Output("page-content", "children"), Input("url", "pathname"))
def render(path):
    if path == "/primitivas":       return pg_primitivas()
    if path == "/riemann":          return pg_riemann()
    if path == "/tfc":              return pg_tfc()
    if path == "/areas":            return pg_areas()
    if path == "/tecnicas":         return pg_tecnicas()
    if path == "/fracoes-parciais": return pg_fracoes_parciais()
    if path == "/aplicacoes":       return pg_aplicacoes()
    if path == "/exercicios":       return pg_exercicios()
    return pg_panorama()

# ═══════════════════════════════════════════
#  CALLBACKS — GRÁFICOS INTERATIVOS
# ═══════════════════════════════════════════

# ── 1. Soma de Riemann ──
@callback(
    Output("graph-riemann", "figure"),
    [Input("slider-riemann-n", "value"),
     Input("dropdown-riemann-func", "value"),
     Input("dropdown-riemann-tipo", "value")],
)
def update_riemann(n, func, tipo):
    funcs = {
        "x2":    (lambda x: x**2,             "f(x) = x²",       0, 1, 1/3),
        "x3":    (lambda x: x**3,             "f(x) = x³",       0, 1, 1/4),
        "expnx": (lambda x: np.exp(-x),       "f(x) = e^(-x)",   0, 2, 1 - np.exp(-2)),
        "sqrtx": (lambda x: np.sqrt(x),       "f(x) = √x",       0, 1, 2/3),
    }
    f, nome, a, b, exato = funcs[func]
    dx = (b - a) / n
    x_smooth = np.linspace(a, b, 500)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_smooth, y=f(x_smooth), mode="lines",
        line=dict(color=BORDO, width=3), name=nome))

    soma = 0
    for i in range(n):
        xi = a + i * dx
        if tipo == "esq":
            ci = xi
        elif tipo == "dir":
            ci = xi + dx
        else:
            ci = xi + dx / 2
        h = f(ci)
        soma += h * dx
        fig.add_shape(type="rect", x0=xi, x1=xi+dx, y0=0, y1=h,
            fillcolor="rgba(21,101,192,0.25)", line=dict(color=AZUL, width=1))

    erro = abs(soma - exato)
    fig.update_layout(
        title=dict(text=f"Soma de Riemann (n={n}): S = {soma:.6f} | Valor exato = {exato:.6f} | Erro = {erro:.2e}",
            font=dict(size=14, color=BORDO_E)),
        xaxis_title="x", yaxis_title="f(x)", font=FONT,
        plot_bgcolor="#fff", xaxis_gridcolor="#ecf0f1", yaxis_gridcolor="#ecf0f1",
        height=500, margin=dict(l=10, r=30, t=60, b=35),
    )
    return fig

# ── 2. Polígono inscrito no círculo ──
@callback(
    Output("graph-poligono", "figure"),
    Input("slider-poligono-n", "value"),
)
def update_poligono(n):
    r = 1
    theta_c = np.linspace(0, 2*np.pi, 500)
    xc = r * np.cos(theta_c)
    yc = r * np.sin(theta_c)

    theta_p = np.linspace(0, 2*np.pi, n+1)
    xp = r * np.cos(theta_p)
    yp = r * np.sin(theta_p)

    area_poligono = (n * r**2 / 2) * np.sin(2 * np.pi / n)
    area_circulo = np.pi * r**2
    erro_pct = abs(area_poligono - area_circulo) / area_circulo * 100

    fig = make_subplots(rows=1, cols=2, subplot_titles=[
        f"Polígono de {n} lados inscrito no círculo",
        "Convergência da área para π"
    ])

    fig.add_trace(go.Scatter(x=xc, y=yc, mode="lines",
        line=dict(color=BORDO, width=2), name="Círculo (r=1)", showlegend=True), row=1, col=1)
    fig.add_trace(go.Scatter(x=xp, y=yp, mode="lines",
        fill="toself", fillcolor="rgba(21,101,192,0.2)",
        line=dict(color=AZUL, width=2), name=f"Polígono ({n} lados)"), row=1, col=1)

    ns = np.arange(3, max(n+1, 52))
    areas = (ns * r**2 / 2) * np.sin(2 * np.pi / ns)
    fig.add_trace(go.Scatter(x=ns, y=areas, mode="lines+markers",
        line=dict(color=AZUL, width=2), marker=dict(size=4),
        name="Área do polígono"), row=1, col=2)
    fig.add_trace(go.Scatter(x=[3, max(n, 51)], y=[np.pi, np.pi], mode="lines",
        line=dict(color=BORDO, width=2, dash="dash"), name="π (área do círculo)"), row=1, col=2)
    fig.add_trace(go.Scatter(x=[n], y=[area_poligono], mode="markers",
        marker=dict(size=12, color=VERDE, symbol="star"), name=f"n={n}"), row=1, col=2)

    fig.update_xaxes(scaleanchor="y", scaleratio=1, row=1, col=1)
    fig.update_layout(
        title=dict(text=f"Área do polígono = {area_poligono:.6f} | π = {np.pi:.6f} | Erro = {erro_pct:.4f}%",
            font=dict(size=14, color=BORDO_E)),
        font=FONT, plot_bgcolor="#fff", height=500,
        margin=dict(l=10, r=30, t=80, b=35),
    )
    return fig

# ── 3. Área entre curvas ──
@callback(
    Output("graph-area", "figure"),
    Input("dropdown-area-func", "value"),
)
def update_area(funcpair):
    configs = {
        "x2_sqrtx": {
            "a": 0, "b": 1,
            "f": lambda x: np.sqrt(x), "g": lambda x: x**2,
            "fn": "√x", "gn": "x²", "area": 1/3,
        },
        "x_x2": {
            "a": 0, "b": 1,
            "f": lambda x: x, "g": lambda x: x**2,
            "fn": "x", "gn": "x²", "area": 1/6,
        },
        "x2_const": {
            "a": 0, "b": np.sqrt(2),
            "f": lambda x: np.full_like(x, 2.0), "g": lambda x: x**2,
            "fn": "2", "gn": "x²", "area": 4*np.sqrt(2)/3,
        },
        "cubica": {
            "a": -1, "b": 2,
            "f": lambda x: np.abs(x**3 - 3*x), "g": lambda x: np.zeros_like(x),
            "fn": "|x³−3x|", "gn": "0", "area": 15/4,
        },
    }
    c = configs[funcpair]
    x = np.linspace(c["a"], c["b"], 500)
    yf = c["f"](x)
    yg = c["g"](x)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=yf, mode="lines",
        line=dict(color=BORDO, width=3), name=f"f(x) = {c['fn']}"))

    if funcpair != "cubica":
        fig.add_trace(go.Scatter(x=x, y=yg, mode="lines",
            line=dict(color=AZUL, width=3), name=f"g(x) = {c['gn']}"))
        fig.add_trace(go.Scatter(
            x=np.concatenate([x, x[::-1]]),
            y=np.concatenate([yf, yg[::-1]]),
            fill="toself", fillcolor="rgba(155,35,53,0.2)",
            line=dict(width=0), name="Área", showlegend=True))
    else:
        x_orig = x
        y_orig = x_orig**3 - 3*x_orig
        fig.add_trace(go.Scatter(x=x_orig, y=y_orig, mode="lines",
            line=dict(color=AZUL, width=2, dash="dash"), name="f(x) = x³−3x (com sinal)"))
        fig.add_trace(go.Scatter(x=x, y=yf, fill="tozeroy",
            fillcolor="rgba(155,35,53,0.2)", line=dict(width=0),
            name="Área = |f(x)|", showlegend=True))

    fig.update_layout(
        title=dict(text=f"Área = {c['area']:.4f}", font=dict(size=16, color=BORDO_E)),
        xaxis_title="x", yaxis_title="y", font=FONT,
        plot_bgcolor="#fff", xaxis_gridcolor="#ecf0f1", yaxis_gridcolor="#ecf0f1",
        height=500, margin=dict(l=10, r=30, t=60, b=35),
    )
    return fig

# ── 4. Visualização de substituição ──
@callback(
    Output("graph-substituicao", "figure"),
    Input("dropdown-subst-ex", "value"),
)
def update_substituicao(ex):
    fig = make_subplots(rows=1, cols=2, subplot_titles=[
        "Domínio original (variável x)", "Domínio transformado (variável u)"
    ])

    if ex == "e3x":
        x = np.linspace(0, 2, 200)
        y_orig = np.exp(3*x)
        u = 3 * x
        y_transf = np.exp(u) / 3
        label_orig = "e^(3x)"
        label_transf = "(1/3)·e^u,  u = 3x"
    elif ex == "x_1x2":
        x = np.linspace(0.1, 3, 200)
        y_orig = x / (1 + x**2)
        u = 1 + x**2
        y_transf = 0.5 / u
        label_orig = "x/(1+x²)"
        label_transf = "(1/2)·(1/u),  u = 1+x²"
    else:  # xex2
        x = np.linspace(0, 2, 200)
        y_orig = x * np.exp(x**2)
        u = x**2
        y_transf = 0.5 * np.exp(u)
        label_orig = "x·e^(x²)"
        label_transf = "(1/2)·e^u,  u = x²"

    fig.add_trace(go.Scatter(x=x, y=y_orig, mode="lines",
        line=dict(color=BORDO, width=3), name=label_orig), row=1, col=1)
    fig.add_trace(go.Scatter(x=u, y=y_transf, mode="lines",
        line=dict(color=AZUL, width=3), name=label_transf), row=1, col=2)

    fig.update_layout(
        font=FONT, plot_bgcolor="#fff", height=450,
        margin=dict(l=10, r=30, t=60, b=35),
        title=dict(text="Substituição: simplificação do integrando",
            font=dict(size=14, color=BORDO_E)),
    )
    fig.update_xaxes(gridcolor="#ecf0f1")
    fig.update_yaxes(gridcolor="#ecf0f1")
    return fig

# ── 5. Decomposição em frações parciais ──
@callback(
    Output("graph-fracoes", "figure"),
    [Input("slider-fp-m", "value"),
     Input("slider-fp-n", "value"),
     Input("slider-fp-alpha", "value"),
     Input("slider-fp-beta", "value")],
)
def update_fracoes(m, n, alpha, beta):
    if alpha == beta:
        beta = alpha + 1

    A = (m * alpha + n) / (alpha - beta)
    B = (m * beta + n) / (beta - alpha)

    margin = 0.3
    x_left  = np.linspace(min(alpha, beta) - 3, alpha - margin, 200)
    x_mid   = np.linspace(alpha + margin, beta - margin, 200)
    x_right = np.linspace(beta + margin, max(alpha, beta) + 3, 200)

    def f_orig(x):
        return (m * x + n) / ((x - alpha) * (x - beta))
    def f_A(x):
        return A / (x - alpha)
    def f_B(x):
        return B / (x - beta)

    fig = go.Figure()
    for seg in [x_left, x_mid, x_right]:
        y_o = f_orig(seg)
        y_a = f_A(seg)
        y_b = f_B(seg)
        y_sum = y_a + y_b
        show = seg is x_left
        fig.add_trace(go.Scatter(x=seg, y=y_o, mode="lines",
            line=dict(color=BORDO, width=3), name="Original (mx+n)/((x-α)(x-β))", showlegend=show, legendgroup="orig"))
        fig.add_trace(go.Scatter(x=seg, y=y_a, mode="lines",
            line=dict(color=AZUL, width=2, dash="dash"), name=f"A/(x-α),  A={A:.2f}", showlegend=show, legendgroup="A"))
        fig.add_trace(go.Scatter(x=seg, y=y_b, mode="lines",
            line=dict(color=VERDE, width=2, dash="dash"), name=f"B/(x-β),  B={B:.2f}", showlegend=show, legendgroup="B"))
        fig.add_trace(go.Scatter(x=seg, y=y_sum, mode="lines",
            line=dict(color=DOURADO, width=2, dash="dot"), name="A/(x-α) + B/(x-β)", showlegend=show, legendgroup="sum"))

    fig.add_vline(x=alpha, line=dict(color="gray", width=1, dash="dash"))
    fig.add_vline(x=beta, line=dict(color="gray", width=1, dash="dash"))

    fig.update_layout(
        title=dict(text=f"({m}x + {n}) / ((x-({alpha}))(x-{beta}))  =  {A:.2f}/(x-({alpha})) + {B:.2f}/(x-{beta})",
            font=dict(size=14, color=BORDO_E)),
        xaxis_title="x", yaxis_title="y", font=FONT,
        yaxis_range=[-10, 10],
        plot_bgcolor="#fff", xaxis_gridcolor="#ecf0f1", yaxis_gridcolor="#ecf0f1",
        height=500, margin=dict(l=10, r=30, t=60, b=35),
    )
    return fig

# ── 6. Tempo ótimo de investimento ──
@callback(
    Output("graph-tempo-otimo", "figure"),
    [Input("slider-tempo-r", "value"),
     Input("dropdown-tempo-vt", "value")],
)
def update_tempo_otimo(r_pct, vt_tipo):
    r = r_pct / 100
    t = np.linspace(0.1, 120, 1000)

    if vt_tipo == "sqrt":
        Vt = 10000 * np.exp(np.sqrt(t))
        dVV = 1 / (2 * np.sqrt(t))
        t_star = 1 / (4 * r**2)
        nome_v = "V(t) = 10000·e^(√t)"
    elif vt_tipo == "linear":
        Vt = 10000 * np.exp(t / 10)
        dVV = np.full_like(t, 0.1)
        t_star = None
        nome_v = "V(t) = 10000·e^(t/10)"
    else:  # log
        Vt = 10000 * np.log(1 + t)
        with np.errstate(divide='ignore', invalid='ignore'):
            log_vals = np.log(1 + t)
            log_vals = np.where(log_vals == 0, 1e-10, log_vals)
            dVV = 1 / ((1 + t) * log_vals)
        try:
            from scipy.optimize import brentq
            t_star = brentq(lambda tt: 1/((1+tt)*np.log(1+tt)) - r, 0.01, 500)
        except Exception:
            t_star = None
        nome_v = "V(t) = 10000·ln(1+t)"

    VPt = Vt * np.exp(-r * t)

    fig = make_subplots(rows=1, cols=2, subplot_titles=[
        "Valor Presente VP(t) = V(t)·e^(-rt)",
        "V'(t)/V(t) vs taxa r"
    ])

    fig.add_trace(go.Scatter(x=t, y=VPt, mode="lines",
        line=dict(color=BORDO, width=3), name="VP(t)"), row=1, col=1)

    if t_star is not None and 0 < t_star < 120:
        if vt_tipo == "sqrt":
            vp_star = 10000 * np.exp(np.sqrt(t_star)) * np.exp(-r * t_star)
        elif vt_tipo == "log":
            vp_star = 10000 * np.log(1 + t_star) * np.exp(-r * t_star)
        else:
            vp_star = 0
        fig.add_trace(go.Scatter(x=[t_star], y=[vp_star], mode="markers+text",
            marker=dict(size=14, color=VERDE, symbol="star"),
            text=[f"t*={t_star:.1f}"], textposition="top center",
            name=f"Ótimo t*={t_star:.1f}"), row=1, col=1)

    t_plot2 = np.linspace(0.5, 100, 500)
    if vt_tipo == "sqrt":
        dVV_plot = 1 / (2 * np.sqrt(t_plot2))
    elif vt_tipo == "linear":
        dVV_plot = np.full_like(t_plot2, 0.1)
    else:
        log_p2 = np.log(1 + t_plot2)
        log_p2 = np.where(log_p2 == 0, 1e-10, log_p2)
        dVV_plot = 1 / ((1 + t_plot2) * log_p2)

    fig.add_trace(go.Scatter(x=t_plot2, y=dVV_plot, mode="lines",
        line=dict(color=AZUL, width=2), name="V'(t)/V(t)"), row=1, col=2)
    fig.add_trace(go.Scatter(x=[0.5, 100], y=[r, r], mode="lines",
        line=dict(color=VERMELHO, width=2, dash="dash"), name=f"r = {r_pct}%"), row=1, col=2)

    if t_star is not None and 0 < t_star < 100:
        fig.add_trace(go.Scatter(x=[t_star], y=[r], mode="markers",
            marker=dict(size=12, color=VERDE, symbol="star"),
            name="Interseção"), row=1, col=2)

    titulo = f"{nome_v},  r = {r_pct}%"
    if t_star is not None and 0 < t_star < 120:
        titulo += f"  |  t* = {t_star:.1f} anos"
    elif vt_tipo == "linear":
        if abs(r - 0.1) < 0.001:
            titulo += "  |  V'/V = r sempre (indiferente)"
        elif r < 0.1:
            titulo += "  |  Nunca vender (V'/V > r)"
        else:
            titulo += "  |  Vender imediatamente (V'/V < r)"

    fig.update_layout(
        title=dict(text=titulo, font=dict(size=14, color=BORDO_E)),
        font=FONT, plot_bgcolor="#fff", height=500,
        margin=dict(l=10, r=30, t=80, b=35),
    )
    fig.update_xaxes(title_text="t (anos)", gridcolor="#ecf0f1")
    fig.update_yaxes(gridcolor="#ecf0f1")
    return fig

# ── 7. Excedente do Consumidor ──
@callback(
    Output("graph-ec", "figure"),
    [Input("slider-ec-q", "value"),
     Input("dropdown-ec-func", "value")],
)
def update_ec(q_star, func_tipo):
    if func_tipo == "linear":
        f_dem = lambda q: np.maximum(100 - 2*q, 0)
        q_max_plot = 55
        q_star = min(q_star, 49)
        p_star = max(100 - 2*q_star, 0.01)
        ec = 100*q_star - q_star**2 - p_star*q_star
        nome = "p = 100 − 2q"
    elif func_tipo == "exp":
        f_dem = lambda q: 50 * np.exp(-0.02*q)
        q_max_plot = 200
        p_star = f_dem(q_star)
        ec = 2500*(1 - np.exp(-0.02*q_star)) - p_star*q_star
        nome = "p = 50·e^(-0.02q)"
    else:  # hiper
        f_dem = lambda q: 200 / (q + 2)
        q_max_plot = 100
        p_star = f_dem(q_star)
        ec = 200*(np.log(q_star + 2) - np.log(2)) - p_star*q_star
        nome = "p = 200/(q+2)"

    q = np.linspace(0.1, q_max_plot, 500)
    p = f_dem(q)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q, y=p, mode="lines",
        line=dict(color=BORDO, width=3), name=nome))

    q_fill = np.linspace(0.1, q_star, 300)
    p_fill = f_dem(q_fill)
    fig.add_trace(go.Scatter(
        x=np.concatenate([q_fill, q_fill[::-1]]),
        y=np.concatenate([p_fill, np.full_like(q_fill, p_star)[::-1]]),
        fill="toself", fillcolor="rgba(65,128,29,0.3)",
        line=dict(width=0), name=f"EC = {ec:.2f}"))

    fig.add_trace(go.Scatter(x=[0, q_max_plot], y=[p_star, p_star], mode="lines",
        line=dict(color=AZUL, width=2, dash="dash"), name=f"p* = {p_star:.2f}"))

    fig.add_trace(go.Scatter(x=[q_star], y=[p_star], mode="markers+text",
        marker=dict(size=12, color=VERDE), text=[f"q*={q_star}"],
        textposition="top right", name="Equilíbrio"))

    fig.update_layout(
        title=dict(text=f"Excedente do Consumidor = {ec:.2f} u.m. | p* = {p_star:.2f}",
            font=dict(size=16, color=BORDO_E)),
        xaxis_title="Quantidade (q)", yaxis_title="Preço (p)", font=FONT,
        plot_bgcolor="#fff", xaxis_gridcolor="#ecf0f1", yaxis_gridcolor="#ecf0f1",
        height=500, margin=dict(l=10, r=30, t=60, b=35),
    )
    return fig

# ── 8. Custo e Receita Marginal ──
@callback(
    Output("graph-custo-receita", "figure"),
    [Input("slider-cr-a", "value"),
     Input("slider-cr-b", "value"),
     Input("slider-cr-p", "value"),
     Input("slider-cr-c0", "value")],
)
def update_custo_receita(a, b, p, c0):
    q_star = max(0, (p - b) / a)
    q = np.linspace(0, max(q_star * 1.8, 10), 500)

    cmg = a * q + b
    rmg = np.full_like(q, p)
    Cq = 0.5 * a * q**2 + b * q + c0
    Rq = p * q
    lucro = Rq - Cq

    fig = make_subplots(rows=1, cols=2, subplot_titles=[
        "Custo Marginal vs Receita Marginal",
        "Custo Total, Receita Total e Lucro"
    ])

    fig.add_trace(go.Scatter(x=q, y=cmg, mode="lines",
        line=dict(color=VERMELHO, width=3), name=f"C'(q) = {a}q + {b}"), row=1, col=1)
    fig.add_trace(go.Scatter(x=q, y=rmg, mode="lines",
        line=dict(color=VERDE, width=3), name=f"R'(q) = {p}"), row=1, col=1)

    if q_star > 0:
        q_lucro = np.linspace(0, q_star, 200)
        fig.add_trace(go.Scatter(
            x=np.concatenate([q_lucro, q_lucro[::-1]]),
            y=np.concatenate([np.full_like(q_lucro, p), (a*q_lucro + b)[::-1]]),
            fill="toself", fillcolor="rgba(65,128,29,0.2)",
            line=dict(width=0), name="Lucro marginal positivo"), row=1, col=1)
        fig.add_trace(go.Scatter(x=[q_star], y=[p], mode="markers+text",
            marker=dict(size=12, color=BORDO, symbol="star"),
            text=[f"q*={q_star:.1f}"], textposition="top right",
            name=f"q* = {q_star:.1f}"), row=1, col=1)

    fig.add_trace(go.Scatter(x=q, y=Cq, mode="lines",
        line=dict(color=VERMELHO, width=2), name="C(q)"), row=1, col=2)
    fig.add_trace(go.Scatter(x=q, y=Rq, mode="lines",
        line=dict(color=VERDE, width=2), name="R(q)"), row=1, col=2)
    fig.add_trace(go.Scatter(x=q, y=lucro, mode="lines",
        line=dict(color=AZUL, width=2, dash="dash"), name="Π(q) = R−C"), row=1, col=2)

    if q_star > 0:
        lucro_star = p * q_star - (0.5*a*q_star**2 + b*q_star + c0)
        fig.add_trace(go.Scatter(x=[q_star], y=[lucro_star], mode="markers+text",
            marker=dict(size=12, color=AZUL, symbol="star"),
            text=[f"Π*={lucro_star:.0f}"], textposition="top left",
            name=f"Lucro máx = {lucro_star:.0f}"), row=1, col=2)

    fig.update_layout(
        title=dict(text=f"C'(q) = {a}q + {b} | R'(q) = {p} | C₀ = {c0} | q* = {q_star:.1f}",
            font=dict(size=14, color=BORDO_E)),
        font=FONT, plot_bgcolor="#fff", height=500,
        margin=dict(l=10, r=30, t=80, b=35),
    )
    fig.update_xaxes(title_text="q", gridcolor="#ecf0f1")
    fig.update_yaxes(gridcolor="#ecf0f1")
    return fig

# ═══════════════════════════════════════════
#  RUN
# ═══════════════════════════════════════════

if __name__ == "__main__":
    app.run(debug=True, port=8060)
