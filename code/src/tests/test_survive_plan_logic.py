import pytest
from unittest.mock import MagicMock
from BDIPlanLogic.SurvivePlanLogic import SurvivePlanLogic


@pytest.fixture
def mock_agent_com_mocks(mocker):
    """
    Cria um mock de agente MESA.
    """

    # 1. Criar o agente principal
    agent = mocker.MagicMock()

    # 2. Criar um mock de 'target'
    mock_target = mocker.MagicMock()
    mock_target.beliefs = {'hp': 100, 'hpMax': 100}
    mock_target.cell = mocker.MagicMock()
    mock_target.cell.coordinate = (1, 0) # Posição padrão do alvo

    # 3. Criar um mock de 'friend'
    mock_friend = mocker.MagicMock()
    mock_friend.beliefs = {'em_batalha': False}
    mock_friend.cell = mocker.MagicMock()
    mock_friend.cell.coordinate = (0, 1) # Posição padrão do amigo

    mock_friend_cell = mocker.MagicMock()
    mock_friend_cell.agents = [mock_friend]

    # 4. Configurar as crenças (beliefs) padrão do agente
    agent.beliefs = {
        'name': 'TestAgent',
        'hp': 100,
        'hpMax': 100,
        'is_alive': True,
        'def': 10,
        'atk': 10,
        'classe': 'Guerreiro',
        'range': 1,
        'iniciativa': 10,
        'displacement': 5,
        'em_batalha': False,
        'num_healing': 2,   
        'healing_item_spot': None,
        'target': None,     
        'color': 'blue'
    }
    
    # 5. Configurar mocks de atributos/métodos
    agent.cell = mocker.MagicMock()
    agent.cell.coordinate = (0, 0) # Posição padrão do agente
    
    # get_friends() retorna uma lista de CÉLULAS que contêm agentes amigos
    agent.get_friends.return_value = [mock_friend_cell] 

    # 6. Disponibilizar os mocks para os testes poderem configurá-los
    agent.MOCKS = {
        'target': mock_target,
        'friend_agent': mock_friend,
        'friend_cell': mock_friend_cell
    }

    return agent


def test_intention_atacar_inimigo(mock_agent_com_mocks):
    """
    Caminho: Sim (em_batalha) -> Sim (target_low_hp) -> Sim (distance == 1)
    """
    agent = mock_agent_com_mocks
    mock_target = agent.MOCKS['target']

    agent.beliefs['em_batalha'] = True
    agent.beliefs['target'] = mock_target
    
    mock_target.beliefs['hp'] = 5
    mock_target.beliefs['hpMax'] = 100
    
    agent.cell.coordinate = (0, 0)
    mock_target.cell.coordinate = (0, 1)

    logic_tree = SurvivePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "ATACAR INIMIGO"


def test_intention_aproximar_se(mock_agent_com_mocks):
    """
    Caminho: Sim (em_batalha) -> Sim (target_low_hp) -> Não (distance > 1)
    """
    agent = mock_agent_com_mocks
    mock_target = agent.MOCKS['target']

    agent.beliefs['em_batalha'] = True
    agent.beliefs['target'] = mock_target
    
    mock_target.beliefs['hp'] = 5 
    
    agent.cell.coordinate = (0, 0)
    mock_target.cell.coordinate = (0, 5)

    logic_tree = SurvivePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "APROXIMAR-SE"


def test_intention_curar_em_batalha(mock_agent_com_mocks):
    """
    Caminho: Sim (em_batalha) -> Não (target_low_hp) -> Sim (have_healing)
    """
    agent = mock_agent_com_mocks
    mock_target = agent.MOCKS['target']

    agent.beliefs['em_batalha'] = True
    agent.beliefs['target'] = mock_target
    agent.beliefs['num_healing'] = 2 
    
    mock_target.beliefs['hp'] = 50 

    logic_tree = SurvivePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "CURAR"


def test_intention_fugir(mock_agent_com_mocks):
    """
    Caminho: Sim (em_batalha) -> Não (target_low_hp) -> Não (have_healing)
    """
    agent = mock_agent_com_mocks
    mock_target = agent.MOCKS['target']

    agent.beliefs['em_batalha'] = True
    agent.beliefs['target'] = mock_target
    agent.beliefs['num_healing'] = 1 
    
    mock_target.beliefs['hp'] = 50 

    logic_tree = SurvivePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "FUGIR"


def test_intention_curar_fora_de_batalha(mock_agent_com_mocks):
    """
    Caminho: Não (em_batalha) -> Sim (have_healing)
    """
    agent = mock_agent_com_mocks
    
    agent.beliefs['em_batalha'] = False 
    agent.beliefs['num_healing'] = 2    

    logic_tree = SurvivePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "CURAR"


def test_intention_obter_cura(mock_agent_com_mocks):
    """
    Caminho: Não (em_batalha) -> Não (have_healing) -> Sim (friend_free) -> Sim (friend_distance == 1)
    """
    agent = mock_agent_com_mocks
    mock_friend = agent.MOCKS['friend_agent']

    agent.beliefs['em_batalha'] = False 
    agent.beliefs['num_healing'] = 0    
    
    mock_friend.beliefs['em_batalha'] = False 
    
    agent.cell.coordinate = (0, 0)
    mock_friend.cell.coordinate = (0, 1) 

    logic_tree = SurvivePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "OBTER CURA"


def test_intention_aproximar_de_amigo(mock_agent_com_mocks):
    """
    Caminho: Não (em_batalha) -> Não (have_healing) -> Sim (friend_free) -> Não (friend_distance > 1)
    """
    agent = mock_agent_com_mocks
    mock_friend = agent.MOCKS['friend_agent']

    agent.beliefs['em_batalha'] = False 
    agent.beliefs['num_healing'] = 0   
    
    mock_friend.beliefs['em_batalha'] = False
    
    agent.cell.coordinate = (0, 0)
    mock_friend.cell.coordinate = (5, 5) 

    logic_tree = SurvivePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "APROXIMAR-SE DE AMIGO"


def test_intention_esperar(mock_agent_com_mocks):
    """
    Caminho: Não (em_batalha) -> Não (have_healing) -> Não (friend_free)
    """
    agent = mock_agent_com_mocks
    mock_friend = agent.MOCKS['friend_agent']

    agent.beliefs['em_batalha'] = False 
    agent.beliefs['num_healing'] = 0   
    
    mock_friend.beliefs['em_batalha'] = True 

    logic_tree = SurvivePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "ESPERAR"


def test_sem_alvo_em_batalha_leva_a_curar(mock_agent_com_mocks):
    """
    Testa o caminho:
    1. Sim (em_batalha)
    2. -> cond_target_low_hp (com target=None, aciona L25, retorna False)
    3. -> Não (caminho do HP não baixo)
    4. -> Sim (have_healing)
    5. = "CURAR"
    """
    agent = mock_agent_com_mocks
    
    agent.beliefs['em_batalha'] = True
    agent.beliefs['target'] = None     
    agent.beliefs['num_healing'] = 2
    
    logic_tree = SurvivePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "CURAR"


def test_alvo_sem_celula_leva_a_aproximar(mock_agent_com_mocks):
    """
    Testa o caminho:
    1. Sim (em_batalha)
    2. -> Sim (target_low_hp)
    3. -> cond_distance (com target.cell=None, aciona L40, retorna False)
    4. -> Não (caminho da distância)
    5. = "APROXIMAR-SE"
    """
    agent = mock_agent_com_mocks
    mock_target = agent.MOCKS['target']

    agent.beliefs['em_batalha'] = True
    agent.beliefs['target'] = mock_target
    
    mock_target.beliefs['hp'] = 5      
    mock_target.cell = None            

    logic_tree = SurvivePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "APROXIMAR-SE"


def test_sem_amigos_leva_a_esperar(mock_agent_com_mocks):
    """
    Testa o caminho:
    1. Não (em_batalha)
    2. -> Não (have_healing)
    3. -> cond_friend_free (com get_friends=[], aciona L44, retorna False)
    4. -> Não (caminho do amigo livre)
    5. = "ESPERAR"
    """
    agent = mock_agent_com_mocks

    agent.beliefs['em_batalha'] = False
    agent.beliefs['num_healing'] = 0    
    
    agent.get_friends.return_value = [] 

    logic_tree = SurvivePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "ESPERAR"


def test_distancia_amigo_none_leva_a_aproximar_amigo(mocker, mock_agent_com_mocks):
    """
    Testa o caminho:
    1. Não (em_batalha)
    2. -> Não (have_healing)
    3. -> Sim (friend_free)
    4. -> cond_friend_distance (get_distance retorna None, aciona L56, retorna False)
    5. -> Não (caminho da distância == 1)
    6. = "APROXIMAR-SE DE AMIGO"
    """
    agent = mock_agent_com_mocks
    mock_friend = agent.MOCKS['friend_agent']

    agent.beliefs['em_batalha'] = False
    agent.beliefs['num_healing'] = 0
    mock_friend.beliefs['em_batalha'] = False 
    
    mocker.patch('BDIPlanLogic.SurvivePlanLogic.get_distance', return_value=None) 

    logic_tree = SurvivePlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "APROXIMAR-SE DE AMIGO"