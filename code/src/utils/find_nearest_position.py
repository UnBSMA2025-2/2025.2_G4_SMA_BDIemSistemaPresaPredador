def move_to_agent(h, l, ax, ay, bx, by, max_step):
    """
    Move o elemento A em direção a B no tabuleiro, respeitando o limite de movimento.

    Parâmetros:
        h: quantidade de linhas do grid
        l: quantidade de colunas do grid
        pos_a (tuple): posição atual de A -> (linha, coluna)
        pos_b (tuple): posição de B -> (linha, coluna)
        max_step (int): número máximo de blocos que A pode se mover por vez

    Retorna:
        tuple: nova posição de A (linha, coluna)
    """
    # calcula diferença entre A e B
    dx = bx - ax
    dy = by - ay

    # se A já está em B
    if dx == 0 and dy == 0:
        return (ax, ay)

    # normaliza direção (para mover em linha reta na proporção correta)
    dist_total = (dx**2 + dy**2) ** 0.5
    if dist_total == 0:
        return (ax, ay)

    # move na direção de B até o limite max_step
    step_x = dx / dist_total * min(max_step, dist_total)
    step_y = dy / dist_total * min(max_step, dist_total)

    # nova posição (arredondando para blocos do tabuleiro)
    novo_x = int(round(ax + step_x))
    novo_y = int(round(ay + step_y))

    # limita dentro do tabuleiro
    novo_x = max(0, min(h - 1, novo_x))
    novo_y = max(0, min(l - 1, novo_y))

    return (novo_x, novo_y)
