import math

def move_to_agent(h, l, ax, ay, bx, by, max_step):
    """
    Calcula a nova posição de A, movendo-se em direção a B no máximo 'max_step' 
    células, com o objetivo de ficar adjacente a B.

    A distância é medida usando a métrica de Chebyshev (L-infinito), 
    onde a distância entre (x1, y1) e (x2, y2) é max(|x1-x2|, |y1-y2|).
    Isso significa que um movimento diagonal conta como 1 passo.

    Argumentos:
        h (int): Altura do tabuleiro (número de linhas).
        l (int): Largura do tabuleiro (número de colunas).
        ax (int): Posição x atual de A.
        ay (int): Posição y atual de A.
        bx (int): Posição x de B.
        by (int): Posição y de B.
        max_step (int): O número máximo de células (passos) que A pode se mover.

    Retorno:
        tuple[int, int]: A nova posição (x, y) de A.
    """

    # 1. Calcular o vetor e a distância de A para B
    dx = bx - ax
    dy = by - ay

    # Distância de Chebyshev (L-infinito)
    # Esta é a quantidade de "passos" (incluindo diagonais) de A para B.
    dist_para_b = max(abs(dx), abs(dy))

    # 2. Verificar Considerações 1 e 2 (se já adjacente ou no mesmo lugar)
    # Se a distância for 1, A já está adjacente.
    # Se a distância for 0, A está em B (o que a regra 1 proíbe, mas
    # em ambos os casos, A não deve se mover para mais perto).
    if dist_para_b <= 1:
        return (ax, ay)

    # 3. Determinar quantos passos A deve realmente mover
    # O objetivo é alcançar uma distância de 1 (adjacente).
    # Portanto, A quer se mover 'dist_para_b - 1' passos.
    # A só pode se mover no máximo 'max_step' passos.
    passos_a_mover = min(max_step, dist_para_b - 1)

    # 4. Calcular o vetor de movimento real
    # Nós "prendemos" (clamp) o vetor total (dx, dy) ao tamanho de 'passos_a_mover'.
    # Isso move A 'passos_a_mover' na direção de B, lidando corretamente
    # com movimentos diagonais e retos.
    #
    # Ex: A=(0,0), B=(10, 5), max_step=3
    #     dist_para_b = 10
    #     passos_a_mover = min(3, 10 - 1) = 3
    #     move_x = max(-3, min(3, 10)) = 3
    #     move_y = max(-3, min(3, 5)) = 3
    #     Nova Posição: (0+3, 0+3) = (3, 3)
    #
    # Ex: A=(0,0), B=(10, 5), max_step=20
    #     dist_para_b = 10
    #     passos_a_mover = min(20, 10 - 1) = 9
    #     move_x = max(-9, min(9, 10)) = 9
    #     move_y = max(-9, min(9, 5)) = 5
    #     Nova Posição: (0+9, 0+5) = (9, 5) -> Esta é adjacente a B!

    move_x = max(-passos_a_mover, min(passos_a_mover, dx))
    move_y = max(-passos_a_mover, min(passos_a_mover, dy))

    # 5. Calcular a nova posição (antes de verificar os limites)
    new_ax = ax + move_x
    new_ay = ay + move_y

    # 6. Consideração 3: Garantir que a nova posição esteja dentro do tabuleiro
    # As coordenadas são baseadas em índice 0, então os limites são:
    # x: [0, l-1]
    # y: [0, h-1]
    final_ax = max(0, min(l - 1, new_ax))
    final_ay = max(0, min(h - 1, new_ay))

    # Esta lógica garante que, mesmo que o tabuleiro seja limitado, a nova
    # posição de A não será a mesma de B, pois o caso 'dist_para_b <= 1'
    # foi tratado primeiro.
    
    return (final_ax, final_ay)

