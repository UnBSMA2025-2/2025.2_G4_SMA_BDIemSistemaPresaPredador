import math
def get_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    """
    Calcula a distância de Manhattan (em "passos" ou "blocos") 
    entre dois pontos em um grid.
    
    Args:
        ponto_a (tuple): Uma tupla (x1, y1) com as coordenadas do ponto A.
        ponto_b (tuple): Uma tupla (x2, y2) com as coordenadas do ponto B.
        
    Returns:
        int: A distância entre os pontos A e B (em número de passos).
    """
    delta_x = abs(x2 - x1)
    delta_y = abs(y2 - y1)
    
    distancia = delta_x + delta_y
    
    return distancia
