# IA para Jogo Toot and Otto

Este projeto implementa uma Inteligência Artificial para jogar o jogo **Toot and Otto** utilizando o algoritmo Minimax. O projeto permite comparar a eficiência entre o Minimax Puro e o Minimax com Poda Alpha-Beta.

## 📋 Pré-requisitos

- Python 3.x instalado.
- **Graphviz** (Ferramenta de sistema) - Necessário apenas se você quiser renderizar os gráficos localmente ou usar a biblioteca Python `graphviz`.

### Instalação do Graphviz no Sistema

Para que a visualização funcione corretamente (caso decida renderizar), instale o Graphviz no seu sistema operacional:

- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt-get install graphviz
  ```

- **Windows:**
  Baixe o instalador em [graphviz.org](https://graphviz.org/download/).
  *Importante:* Durante a instalação, marque a opção **"Add Graphviz to the system PATH for all users"**.

- **macOS:**
  ```bash
  brew install graphviz
  ```
## � Instalação

1. Clone o repositório (se ainda não tiver):
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd trabalho_ia
   ```

2. (Opcional) Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## �🚀 Como Executar

O script principal é o `toot_otto.py`. Ele deve ser executado via linha de comando (terminal) passando os parâmetros de configuração.

### Sintaxe

```bash
python toot_otto.py <MODO> <PROFUNDIDADE> [VISUALIZAR]
```

### Parâmetros

1. **MODO**: Escolhe o algoritmo.
   - `0`: Minimax Puro (Sem poda).
   - `1`: Minimax com Poda Alpha-Beta (Mais rápido).

2. **PROFUNDIDADE**: Quantos movimentos à frente a IA deve calcular.
   - Exemplo: `4`, `5`, `6`.
   - *Nota:* Profundidades acima de 5 podem demorar muito no modo sem poda.

3. **VISUALIZAR** (Opcional): Gera um arquivo de visualização da árvore.
   - `0`: Não gerar (Padrão).
   - `1`: Gerar arquivo `.dot`.

---

## 💡 Exemplos de Uso

### 1. Rodar Minimax Puro com profundidade 4
```bash
python toot_otto.py 0 4
```

### 2. Rodar Alpha-Beta com profundidade 5 (Recomendado)
```bash
python toot_otto.py 1 5
```

### 3. Gerar visualização da árvore (Profundidade baixa recomendada)
```bash
python toot_otto.py 1 3 1
```
Isso irá gerar um arquivo `arvore_alphabeta.dot` ou `arvore_minimax.dot`.

---

## 🌳 Como ver a Árvore Gerada

Se você usou a opção de visualização, um arquivo `.dot` foi criado. Para ver o gráfico:

1. Abra o conteúdo do arquivo `.dot` em um editor de texto.
2. Copie todo o texto.
3. Cole no site: [GraphvizOnline](https://dreampuf.github.io/GraphvizOnline/).

---

## 🧠 Como funciona a Heurística

A IA avalia o tabuleiro analisando todas as janelas possíveis de 4 células (horizontal, vertical e diagonal). A pontuação é atribuída com base nos padrões encontrados:

| Padrão (Exemplos) | Pontos (TOOT) | Pontos (OTTO) | Significado |
| :--- | :--- | :--- | :--- |
| **Vitória** (`TOOT`) | **+10.000** | | Vitória garantida. |
| **Derrota** (`OTTO`) | | **-10.000** | Derrota garantida. |
| **Ameaça Forte** (`TOO.`, `T.OT`) | **+100** | | Falta 1 peça para ganhar. |
| **Ameaça Inimiga** (`OTT.`, `O.TO`) | | **-100** | Inimigo ganha na próxima. |
| **Potencial** (`TO..`, `T..T`) | **+5** | | Sequência de 2 peças. |
| **Potencial Inimigo** (`OT..`, `O..O`) | | **-5** | Sequência inimiga de 2 peças. |
| **Início** (`T...`) | **+1** | | Peça única bem posicionada. |
| **Início Inimigo** (`O...`) | | **-1** | Peça única inimiga. |

O **Score Final** é a soma de todas as janelas do tabuleiro.
- **Positivo**: Vantagem para TOOT.
- **Negativo**: Vantagem para OTTO.
- **Zero**: Jogo equilibrado.

---

## 📊 Entendendo o Resultado

O programa exibirá:
- **Tempo de execução**: Quanto tempo demorou para calcular.
- **Nós gerados**: Quantos estados do tabuleiro foram analisados.
- **Score final**: A avaliação do tabuleiro (+ é bom para TOOT, - é bom para OTTO).

Se você rodar os dois modos com a mesma profundidade, o **Score final** deve ser idêntico, mas o **Tempo** e **Nós gerados** serão muito menores no Alpha-Beta.
