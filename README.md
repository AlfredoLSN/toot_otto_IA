# IA para Jogo Toot and Otto

Este projeto implementa uma Inteligência Artificial para jogar o jogo **Toot and Otto** utilizando o algoritmo Minimax. O projeto permite comparar a eficiência entre o Minimax Puro e o Minimax com Poda Alpha-Beta.

## 📋 Pré-requisitos

- Python 3.x instalado.

## 🚀 Como Executar

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

## 📊 Entendendo o Resultado

O programa exibirá:
- **Tempo de execução**: Quanto tempo demorou para calcular.
- **Nós gerados**: Quantos estados do tabuleiro foram analisados.
- **Score final**: A avaliação do tabuleiro (+ é bom para TOOT, - é bom para OTTO).

Se você rodar os dois modos com a mesma profundidade, o **Score final** deve ser idêntico, mas o **Tempo** e **Nós gerados** serão muito menores no Alpha-Beta.
