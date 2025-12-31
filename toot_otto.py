import time
import sys

class OttoTootIA:
    def __init__(self, visualizar=False):
        # Configuração do Tabuleiro 4x6
        self.rows = 4
        self.cols = 6
        # Cria matriz vazia ('.' representa espaço vazio)
        self.board = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Contador estatístico
        self.nos_visitados = 0
        
        # Estoque de peças (Regra Oficial: 6 Ts e 6 Os para cada jogador)
        self.pieces_count = {
            'TOOT': {'T': 6, 'O': 6},
            'OTTO': {'T': 6, 'O': 6}
        }
        
        # Visualização
        self.visualizar = visualizar
        self.node_count = 0
        self.dot_lines = []
        if self.visualizar:
            self.dot_lines.append("digraph G {")
            self.dot_lines.append("  node [shape=box, style=filled, fontname=\"Arial\"];")

    def log_node(self, node_id, label, color="white", shape="box"):
        if not self.visualizar: return
        # Limite de segurança para não travar em árvores gigantes
        if len(self.dot_lines) > 50000: return 
        self.dot_lines.append(f'  {node_id} [label="{label}", fillcolor="{color}", shape="{shape}"];')

    def log_edge(self, parent_id, child_id, label):
        if not self.visualizar: return
        if len(self.dot_lines) > 50000: return
        self.dot_lines.append(f'  {parent_id} -> {child_id} [label="{label}", fontsize=10];')

    def save_dot_file(self, filename="arvore_decisao.dot"):
        if not self.visualizar: return
        self.dot_lines.append("}")
        with open(filename, "w") as f:
            f.write("\n".join(self.dot_lines))
        print(f"\n[VISUALIZAÇÃO] Arquivo '{filename}' gerado com sucesso!")
        print("Use https://dreampuf.github.io/GraphvizOnline/ para visualizar.")

    # --- LÓGICA DO TABULEIRO (FÍSICA) ---

    def is_valid_move(self, col):
        """Verifica se a coluna aceita peças (não está cheia)"""
        return 0 <= col < self.cols and self.board[0][col] == '.'

    def make_move(self, col, piece, player):
        """
        Aplica a gravidade: a peça cai até a última linha disponível.
        Retorna a linha onde a peça parou (para facilitar o undo).
        Atualiza contagem de peças.
        """
        self.pieces_count[player][piece] -= 1
        for r in range(self.rows - 1, -1, -1):
            if self.board[r][col] == '.':
                self.board[r][col] = piece
                return r
        return -1

    def undo_move(self, col, row, piece, player):
        """Remove a peça (Backtracking) e restaura contagem"""
        self.board[row][col] = '.'
        self.pieces_count[player][piece] += 1

    def get_valid_moves(self, player):
        """
        Gera todos os filhos possíveis.
        Considera o limite de peças de cada jogador.
        """
        moves = []
        available_pieces = []
        if self.pieces_count[player]['T'] > 0: available_pieces.append('T')
        if self.pieces_count[player]['O'] > 0: available_pieces.append('O')

        for col in range(self.cols):
            if self.is_valid_move(col):
                for p in available_pieces:
                    moves.append((col, p))
        return moves

    # --- HEURÍSTICA (INTELIGÊNCIA) ---

    def evaluate_window(self, window):
        """
        Avalia um grupo de 4 células.
        Pontos positivos favorecem TOOT (Maximizador).
        Pontos negativos favorecem OTTO (Minimizador).
        """
        score = 0
        seq = "".join(window)

        # TOOT (Objetivo: T-O-O-T)
        if seq == "TOOT": return 10000
        if seq == "TOO." or seq == ".OOT" or seq == "T.OT" or seq == "TO.T": score += 100
        if seq == "TO.." or seq == "..OT" or seq == "T..T": score += 5
        if seq == "T..." or seq == ".O.." or seq == "..O." or seq == "...T": score += 1

        # OTTO (Objetivo: O-T-T-O)
        if seq == "OTTO": return -10000
        if seq == "OTT." or seq == ".TTO" or seq == "O.TO" or seq == "OT.O": score -= 100
        if seq == "OT.." or seq == "..TO" or seq == "O..O": score -= 5
        if seq == "O..." or seq == ".T.." or seq == "..T." or seq == "...O": score -= 1

        return score

    def evaluate_state(self):
        """Calcula a pontuação total do tabuleiro atual."""
        score = 0

        # Horizontal
        for r in range(self.rows):
            for c in range(self.cols - 3):
                window = self.board[r][c:c+4]
                score += self.evaluate_window(window)

        # Vertical
        for c in range(self.cols):
            for r in range(self.rows - 3):
                window = [self.board[r+i][c] for i in range(4)]
                score += self.evaluate_window(window)

        # Diagonal Positiva (/)
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [self.board[r+i][c+i] for i in range(4)]
                score += self.evaluate_window(window)

        # Diagonal Negativa (\)
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [self.board[r+3-i][c+i] for i in range(4)]
                score += self.evaluate_window(window)

        return score

    # --- ALGORITMO 1: MINIMAX PURO (SEM PODA) ---
    
    def minimax(self, depth, is_maximizing, parent_id=None, move_from_parent=""):
        self.nos_visitados += 1
        my_id = self.node_count
        self.node_count += 1

        # Registra a aresta vinda do pai
        if parent_id is not None:
            self.log_edge(parent_id, my_id, move_from_parent)

        if depth == 0:
            val = self.evaluate_state()
            self.log_node(my_id, f"Leaf\nScore: {val}", "lightyellow", "ellipse")
            return val

        current_player = 'TOOT' if is_maximizing else 'OTTO'
        valid_moves = self.get_valid_moves(current_player)
        
        # Se não houver movimentos (tabuleiro cheio), avalia
        if not valid_moves:
            val = self.evaluate_state()
            self.log_node(my_id, f"End\nScore: {val}", "gray")
            return val

        if is_maximizing:
            max_eval = -float('inf')
            for col, piece in valid_moves:
                row = self.make_move(col, piece, current_player)
                eval = self.minimax(depth - 1, False, my_id, f"{piece} em {col}")
                self.undo_move(col, row, piece, current_player)
                max_eval = max(max_eval, eval)
            
            self.log_node(my_id, f"MAX (D{depth})\nBest: {max_eval}", "lightblue")
            return max_eval
        else:
            min_eval = float('inf')
            for col, piece in valid_moves:
                row = self.make_move(col, piece, current_player)
                eval = self.minimax(depth - 1, True, my_id, f"{piece} em {col}")
                self.undo_move(col, row, piece, current_player)
                min_eval = min(min_eval, eval)
            
            self.log_node(my_id, f"MIN (D{depth})\nBest: {min_eval}", "lightpink")
            return min_eval

    # --- ALGORITMO 2: MINIMAX COM PODA ALPHA-BETA ---

    def minimax_alpha_beta(self, depth, alpha, beta, is_maximizing, parent_id=None, move_from_parent=""):
        self.nos_visitados += 1
        my_id = self.node_count
        self.node_count += 1

        # Registra a aresta vinda do pai
        if parent_id is not None:
            self.log_edge(parent_id, my_id, move_from_parent)

        if depth == 0:
            val = self.evaluate_state()
            self.log_node(my_id, f"Leaf\nScore: {val}", "lightyellow", "ellipse")
            return val

        current_player = 'TOOT' if is_maximizing else 'OTTO'
        valid_moves = self.get_valid_moves(current_player)
        
        if not valid_moves:
            val = self.evaluate_state()
            self.log_node(my_id, f"End\nScore: {val}", "gray")
            return val

        if is_maximizing:
            max_eval = -float('inf')
            for col, piece in valid_moves:
                row = self.make_move(col, piece, current_player)
                eval = self.minimax_alpha_beta(depth - 1, alpha, beta, False, my_id, f"{piece} em {col}")
                self.undo_move(col, row, piece, current_player)
                
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                
                # PODA: O minimizador (pai) não vai deixar esse caminho acontecer
                if beta <= alpha:
                    self.log_node(my_id, f"MAX (D{depth})\nPruned!", "orange") # Indica poda visualmente? Ou apenas o nó normal
                    # Na verdade, se podou, não visitamos os outros filhos.
                    # O nó atual ainda retorna max_eval.
                    break 
            
            self.log_node(my_id, f"MAX (D{depth})\nBest: {max_eval}\nα={alpha} β={beta}", "lightblue")
            return max_eval
        else:
            min_eval = float('inf')
            for col, piece in valid_moves:
                row = self.make_move(col, piece, current_player)
                eval = self.minimax_alpha_beta(depth - 1, alpha, beta, True, my_id, f"{piece} em {col}")
                self.undo_move(col, row, piece, current_player)
                
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                
                # PODA: O maximizador (pai) não vai deixar esse caminho acontecer
                if beta <= alpha:
                    break
            
            self.log_node(my_id, f"MIN (D{depth})\nBest: {min_eval}\nα={alpha} β={beta}", "lightpink")
            return min_eval

# --- BLOCO DE EXECUÇÃO ---

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python toot_otto.py <modo> <profundidade> [visualizar]")
        print("Modo 0: Minimax Puro")
        print("Modo 1: Minimax com Poda Alpha-Beta")
        print("Visualizar (opcional): 1 para gerar arquivo .dot")
        print("Exemplo: python toot_otto.py 1 5 1")
        sys.exit(1)

    try:
        modo = int(sys.argv[1])
        profundidade = int(sys.argv[2])
        visualizar = False
        if len(sys.argv) > 3 and int(sys.argv[3]) == 1:
            visualizar = True
            if profundidade > 4:
                print("AVISO: Visualização com profundidade > 4 pode gerar arquivos gigantes.")
                print("Recomendado usar profundidade 2 ou 3 para visualizar.")
                time.sleep(2)
    except ValueError:
        print("Erro: Parâmetros devem ser números inteiros.")
        sys.exit(1)
    
    print(f"=== INICIANDO SIMULAÇÃO TOOT AND OTTO ===")
    print(f"Profundidade da Árvore: {profundidade}")
    print(f"Fator de Ramificação Médio: ~12 movimentos por nó\n")

    if modo == 0:
        # 1. Executando Minimax Puro
        print("1. Rodando Minimax PURO...")
        start_time = time.time()
        
        jogo_mm = OttoTootIA(visualizar=visualizar)
        score_mm = jogo_mm.minimax(profundidade, True) # True = Começa Maximizing
        
        end_time = time.time()
        tempo_mm = end_time - start_time
        total_mm = jogo_mm.nos_visitados
        
        print(f"   -> Concluído em {tempo_mm:.2f} segundos")
        print(f"   -> Nós gerados: {total_mm}")
        print(f"   -> Score final calculado: {score_mm}")
        
        if visualizar:
            jogo_mm.save_dot_file("arvore_minimax.dot")

    elif modo == 1:
        # 2. Executando Alpha-Beta
        print("2. Rodando Poda ALPHA-BETA...")
        start_time = time.time()
        
        jogo_ab = OttoTootIA(visualizar=visualizar)
        # Alpha = -Infinito, Beta = +Infinito
        score_ab = jogo_ab.minimax_alpha_beta(profundidade, -float('inf'), float('inf'), True)
        
        end_time = time.time()
        tempo_ab = end_time - start_time
        total_ab = jogo_ab.nos_visitados
        
        print(f"   -> Concluído em {tempo_ab:.2f} segundos")
        print(f"   -> Nós gerados: {total_ab}")
        print(f"   -> Score final calculado: {score_ab}")
        
        if visualizar:
            jogo_ab.save_dot_file("arvore_alphabeta.dot")

    else:
        print("Modo inválido. Use 0 para Minimax Puro ou 1 para Alpha-Beta.")