import pytest
from utils.get_distance import get_distance


@pytest.mark.parametrize("x1, y1, x2, y2, expected", [
    # Cenário 1: Pontos idênticos (Distância Zero)
    (5, 5, 5, 5, 0),
    (0, 0, 0, 0, 0),
    (-3, -3, -3, -3, 0),

    # Cenário 2: Movimento Puramente Horizontal
    (0, 0, 5, 0, 5),  # Direita
    (5, 0, 0, 0, 5),  # Esquerda

    # Cenário 3: Movimento Puramente Vertical
    (0, 0, 0, 5, 5),  # Cima
    (0, 5, 0, 0, 5),  # Baixo

    # Cenário 4: Movimento Diagonal (Misto)
    (1, 2, 4, 6, 7),   # (delta_x=3) + (delta_y=4) = 7
    (10, 5, 1, 2, 12), # (delta_x=9) + (delta_y=3) = 12

    # Cenário 5: Coordenadas Negativas
    (-1, -1, -5, -5, 8), # (delta_x=4) + (delta_y=4) = 8
    
    # Cenário 6: Cruzando a Origem (Negativo para Positivo)
    (-2, -2, 2, 2, 8)    # (delta_x=4) + (delta_y=4) = 8
])


def test_get_distance_varios_cenarios(x1, y1, x2, y2, expected):
    """
    Testa a função get_distance com um conjunto variado de cenários.
    """
    # Teste de simetria (A->B deve ser igual a B->A)
    dist_ab = get_distance(x1, y1, x2, y2)
    dist_ba = get_distance(x2, y2, x1, y1)
    
    assert dist_ab == expected
    assert dist_ba == expected