def get_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    """
    Calcula a distância de Manhattan (em "passos" ou "blocos") 
    entre dois pontos em um grid.
    
    Args:
        x1 (int): Coordenada X do ponto A.
        y1 (int): Coordenada Y do ponto A.
        x2 (int): Coordenada X do ponto B.
        y2 (int): Coordenada Y do ponto B.
        
    Returns:
        int: A distância entre os pontos A e B (em número de passos).
    """
    delta_x = abs(x2 - x1)
    delta_y = abs(y2 - y1)
    
    distancia = delta_x + delta_y
    
    return distancia