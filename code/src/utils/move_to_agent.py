import math

def move_to_agent(h, l, ax, ay, bx, by, max_step):
    """
    Calcula a nova posição de A, movendo-se em direção a B, respeitando
    um número máximo de passos (max_step) e as fronteiras do tabuleiro.

    A distância usada é a Distância de Chebyshev (movimento de "rei" no
    xadrez), onde mover-se na diagonal custa 1 passo.

    A posição final de A (A') tentará estar a uma distância de 1 de B,
    e A' não pode ser igual a B.

    Args:
        h: Altura (height) do tabuleiro (número de linhas, indexadas de 0 a h-1).
        l: Largura (width) do tabuleiro (número de colunas, indexadas de 0 a l-1).
        ax: Posição X inicial de A.
        ay: Posição Y inicial de A.
        bx: Posição X de B.
        by: Posição Y de B.
        max_step: O número máximo de "células" (passos) que A pode se mover.

    Returns:
        Uma tupla (int, int) representando a nova posição (x, y) de A.
    """

    # --- 1. Calcular o vetor e a distância de A para B ---
    # A distância de Chebyshev (L-infinito) é o máximo das
    # diferenças absolutas das coordenadas.
    vx = bx - ax
    vy = by - ay
    distancia = max(abs(vx), abs(vy))

    # --- 2. Lidar com casos base (Constraints 1 e 2) ---

    # Caso 1: A e B já estão na mesma posição (distancia == 0).
    # Constraint 1 diz que não podem ocupar a msm posição (na nova rodada).
    # A *deve* se mover para uma posição adjacente (distância 1).
    if distancia == 0:
        if max_step == 0:
            # Impossível mover, falha em satisfazer a constraint 1.
            # Retorna a posição atual como única opção.
            return (ax, ay)
        
        # Tenta mover 1 passo para (ax+1, ay) e valida
        # contra as bordas do tabuleiro.
        # max(0, ...) garante que não seja < 0
        # min(l-1, ...) garante que não seja >= l
        
        # Tenta mover para a direita
        new_ax = max(0, min(l - 1, ax + 1))
        new_ay = max(0, min(h - 1, ay))
        if (new_ax, new_ay) != (ax, ay):
            return (new_ax, new_ay)
            
        # Tenta mover para a esquerda
        new_ax = max(0, min(l - 1, ax - 1))
        new_ay = max(0, min(h - 1, ay))
        if (new_ax, new_ay) != (ax, ay):
            return (new_ax, new_ay)

        # Tenta mover para baixo
        new_ax = max(0, min(l - 1, ax))
        new_ay = max(0, min(h - 1, ay + 1))
        if (new_ax, new_ay) != (ax, ay):
            return (new_ax, new_ay)
            
        # Tenta mover para cima (única opção restante)
        new_ax = max(0, min(l - 1, ax))
        new_ay = max(0, min(h - 1, ay - 1))
        return (new_ax, new_ay) # Retorna (ax, ay) se for um tabuleiro 1x1

    # Caso 2: A já está adjacente a B (distancia == 1).
    # Este é o objetivo (Constraint 2). A não precisa se mover.
    if distancia == 1:
        return (ax, ay)

    # --- 3. Calcular movimento (distancia > 1) ---

    # A quer se mover para uma distância de 1, então ela
    # "quer" dar `distancia - 1` passos.
    passos_desejados = distancia - 1

    # A só pode dar o mínimo entre o que quer e o que pode (max_step).
    passos_a_dar = min(max_step, passos_desejados)

    # Se max_step for 0, passos_a_dar será 0.
    if passos_a_dar == 0:
        return (ax, ay)

    # --- 4. Calcular a nova posição (sem fronteiras) ---
    # Usamos uma proporção para mover A ao longo do "vetor" (vx, vy)
    # no espaço de Chebyshev. O `round` lida com o movimento
    # diagonal (ex: mover 3 passos para (10, 5) resulta em (3, 2)).
    
    # É crucial usar divisão flutuante aqui.
    proporcao_movimento = passos_a_dar / distancia
    
    # round() nativo do Python arredonda para o inteiro mais próximo.
    # (ex: round(1.5) == 2, round(1.49) == 1)
    # Convertemos para int para segurança.
    new_ax = ax + round(vx * proporcao_movimento)
    new_ay = ay + round(vy * proporcao_movimento)

    # --- 5. Aplicar fronteiras (Constraint 3) ---
    # Garante que a nova posição esteja dentro do tabuleiro h x l.
    
    final_ax = max(0, min(l - 1, int(new_ax)))
    final_ay = max(0, min(h - 1, int(new_ay)))

    # A lógica garante que nunca pousaremos em B, pois
    # `passos_a_dar` é no máximo `distancia - 1`.
    return (final_ax, final_ay)

