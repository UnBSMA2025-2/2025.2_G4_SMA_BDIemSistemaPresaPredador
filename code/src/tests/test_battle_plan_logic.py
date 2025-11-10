import pytest
from unittest.mock import MagicMock
from BDIPlanLogic.BattlePlanLogic import BattlePlanLogic


@pytest.fixture
def mock_battle_agent(mocker):
    """
    Cria um mock de agente MESA para testar o BattlePlanLogic.
    """
    # 1. Criar o agente principal
    agent = mocker.MagicMock()

    # --- Mocks de Agentes Externos ---
    
    # 2. Criar um mock de 'target' (alvo)
    mock_target = mocker.MagicMock()
    mock_target.cell = mocker.MagicMock()
    mock_target.cell.coordinate = (1, 0) # Posição padrão do alvo

    # 3. Criar um mock de 'enemy' (vizinho)
    mock_enemy = mocker.MagicMock()
    mock_enemy.type = 'ENEMY' # (Qualquer coisa que não seja 'CHARACTER')

    # 4. Criar um mock de 'friend' (vizinho)
    mock_friend = mocker.MagicMock()
    mock_friend.type = 'CHARACTER'
    mock_friend.beliefs = {'em_batalha': False} # Padrão: amigo não está em batalha

    # --- Mocks de Células (para vizinhança) ---
    
    cell_empty = mocker.MagicMock()
    cell_empty.agents = []

    cell_with_enemy = mocker.MagicMock()
    cell_with_enemy.agents = [mock_enemy]
    
    cell_with_friend = mocker.MagicMock()
    cell_with_friend.agents = [mock_friend]

    # 5. Configurar o agente principal
    agent.beliefs = {
        'target': None,      # Padrão: sem alvo
        'range': 1,
        'displacement': 5
    }
    
    agent.cell = mocker.MagicMock()
    agent.cell.coordinate = (0, 0) # Posição padrão do agente

    # Simula a vizinhança imediata (para cond_is_surrounded)
    agent.cell.neighborhood.cells = [cell_empty] # Padrão: não cercado
    
    # Simula a vizinhança de "displacement" (para cond_friend_attacking)
    # .get_neighborhood() retorna um objeto que tem um atributo 'cells'
    agent.cell.get_neighborhood.return_value.cells = [cell_empty] # Padrão: sem amigos atacando

    # 6. Disponibilizar os mocks para os testes poderem configurá-los
    agent.MOCKS = {
        'target': mock_target,
        'enemy_agent': mock_enemy,
        'friend_agent': mock_friend,
        'cell_empty': cell_empty,
        'cell_with_enemy': cell_with_enemy,
        'cell_with_friend': cell_with_friend
    }

    return agent


def test_intention_atacar_inimigo(mock_battle_agent):
    """
    Caminho: Sim (cond_has_target) -> Sim (cond_enable_atk_enemy)
    """
    agent = mock_battle_agent
    mock_target = agent.MOCKS['target']

    agent.beliefs['target'] = mock_target
    agent.beliefs['range'] = 1
    
    agent.cell.coordinate = (0, 0)
    mock_target.cell.coordinate = (0, 3) 
    
    logic_tree = BattlePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "ATACAR INIMIGO"


def test_intention_aproximar_se(mock_battle_agent):
    """
    Caminho: Sim (cond_has_target) -> Não (cond_enable_atk_enemy)
    """
    agent = mock_battle_agent
    mock_target = agent.MOCKS['target']

    agent.beliefs['target'] = mock_target
    agent.beliefs['range'] = 1
    
    agent.cell.coordinate = (0, 0)
    mock_target.cell.coordinate = (0, 4) 
    
    logic_tree = BattlePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "APROXIMAR-SE"


def test_intention_definir_alvo(mock_battle_agent):
    """
    Caminho: Não (cond_has_target) -> Sim (cond_is_surrounded)
    """
    agent = mock_battle_agent
    cell_with_enemy = agent.MOCKS['cell_with_enemy']

    agent.beliefs['target'] = None 
    
    agent.cell.neighborhood.cells = [cell_with_enemy]
    
    logic_tree = BattlePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "DEFINIR ALVO"


def test_intention_definir_alvo_do_amigo(mock_battle_agent):
    """
    Caminho: Não (cond_has_target) -> Não (cond_is_surrounded) -> Sim (cond_friend_attacking)
    """
    agent = mock_battle_agent
    mock_friend = agent.MOCKS['friend_agent']
    cell_with_friend = agent.MOCKS['cell_with_friend']

    agent.beliefs['target'] = None 
    
    agent.cell.neighborhood.cells = [agent.MOCKS['cell_empty']]
    
    mock_friend.beliefs['em_batalha'] = True
    
    agent.cell.get_neighborhood.return_value.cells = [cell_with_friend]
    
    logic_tree = BattlePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "DEFINIR ALVO DO AMIGO"


def test_intention_definir_outro_alvo(mock_battle_agent):
    """
    Caminho: Não (cond_has_target) -> Não (cond_is_surrounded) -> Não (cond_friend_attacking)
    """
    agent = mock_battle_agent
    mock_friend = agent.MOCKS['friend_agent']
    cell_with_friend = agent.MOCKS['cell_with_friend']

    agent.beliefs['target'] = None 
    
    agent.cell.neighborhood.cells = [agent.MOCKS['cell_empty']]
    
    mock_friend.beliefs['em_batalha'] = False
    
    agent.cell.get_neighborhood.return_value.cells = [cell_with_friend]
    
    logic_tree = BattlePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "DEFINIR OUTRO ALVO"


def test_coverage_target_sem_celula_leva_a_aproximar(mock_battle_agent):
    """
    Testa o 'if enemy.cell is not None' em 'cond_enable_atk_enemy'.
    Caminho: Sim (target) -> Não (enable_atk, porque target.cell is None)
    """
    agent = mock_battle_agent
    mock_target = agent.MOCKS['target']

    agent.beliefs['target'] = mock_target
    mock_target.cell = None 
    
    logic_tree = BattlePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "APROXIMAR-SE"


def test_coverage_agente_sem_celula_nao_quebra_arvore(mock_battle_agent):
    """
    Testa 'if agent is not None and agent.cell is not None' em 
    'cond_is_surrounded' E 'cond_friend_attacking'.
    Caminho: Não (target) -> Não (surrounded, cell=None) -> Não (friend_attacking, cell=None)
    """
    agent = mock_battle_agent
    agent.beliefs['target'] = None
    agent.cell = None 
    
    logic_tree = BattlePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "DEFINIR OUTRO ALVO"