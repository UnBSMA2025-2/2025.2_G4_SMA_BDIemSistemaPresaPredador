def move_to_agent(h, l, ax, ay, bx, by, max_step):
    """
    Calcula a nova posição de A, movendo-se em direção a B, respeitando
    um número máximo de passos (max_step) e as fronteiras do grid.

    Args:
        h: Altura (height) do grid (número de linhas, indexadas de 0 a h-1).
        l: Largura (width) do grid (número de colunas, indexadas de 0 a l-1).
        ax: Posição X inicial de A.
        ay: Posição Y inicial de A.
        bx: Posição X de B.
        by: Posição Y de B.
        max_step: O número máximo de "células" (passos) que A pode se mover.

    Returns:
        Uma tupla (int, int) representando a nova posição (x, y) de A.
    """
    vx = bx - ax
    vy = by - ay
    # print("Vetor de movimento (vx, vy):")
    # print(vx, vy)
    distancia = max(abs(vx), abs(vy))
    
    if distancia == 0:
        if max_step == 0:
            return (ax, ay)
        
        new_ax = max(0, min(l - 1, ax + 1))
        new_ay = max(0, min(h - 1, ay))
        if (new_ax, new_ay) != (ax, ay):
            return (new_ax, new_ay)
            
        new_ax = max(0, min(l - 1, ax - 1))
        new_ay = max(0, min(h - 1, ay))
        if (new_ax, new_ay) != (ax, ay):
            return (new_ax, new_ay)

        new_ax = max(0, min(l - 1, ax))
        new_ay = max(0, min(h - 1, ay + 1))
        if (new_ax, new_ay) != (ax, ay):
            return (new_ax, new_ay)
            
        new_ax = max(0, min(l - 1, ax))
        new_ay = max(0, min(h - 1, ay - 1))
        return (new_ax, new_ay) 

    # print(f"Distância entre A e B: {distancia}")
    if distancia == 1:
        try:
            # print(ax, ay)

            new_ax = ax
            new_ay = ay
            
            if (vy != 0):
                new_ay = ay + (1 if vy > 0 else -1)
            
            if (vx != 0):
                new_ax = ax + (1 if vx > 0 else -1)

            final_ax = max(0, min(l - 1, new_ax))
            final_ay = max(0, min(h - 1, new_ay))

            # print(f"Movendo (dist=1) para ({final_ax}, {final_ay})")
            return (final_ax, final_ay)

        except Exception as e:
            # (ex: um TypeError se 'h' for None)
            print(f"ATENÇÃO [move_to_agent]: Ocorreu um erro inesperado ao calcular movimento adjacente.")
            print(f"   Erro: {e}")
            print(f"   Valores: ax={ax}, ay={ay}, h={h}, l={l}, vx={vx}, vy={vy}")
            return (ax, ay)

    passos_desejados = distancia - 1

    passos_a_dar = min(max_step, passos_desejados)

    if passos_a_dar == 0:
        return (ax, ay)

    proporcao_movimento = passos_a_dar / distancia
    
    new_ax = ax + round(vx * proporcao_movimento)
    new_ay = ay + round(vy * proporcao_movimento)

    final_ax = max(0, min(l - 1, int(new_ax)))
    final_ay = max(0, min(h - 1, int(new_ay)))

    # print(f"Movendo de ({ax}, {ay}) para ({final_ax}, {final_ay}) com max_step={max_step}")

    return (final_ax, final_ay)

