import pytest
from unittest.mock import MagicMock
from BDIPlanLogic.RetaliateAttackPlanLogic import RetaliateAttackPlanLogic


@pytest.fixture
def mock_retaliate_agent(mocker):
    """
    Cria um mock de agente MESA para testar o RetaliateAttackPlanLogic.
    """
    # 1. Criar o agente principal
    agent = mocker.MagicMock()

    # 2. Criar um mock de 'target'
    mock_target = mocker.MagicMock()
    mock_target.cell = mocker.MagicMock()
    mock_target.cell.coordinate = (1, 0) # Posição padrão do alvo

    # 3. Configurar as crenças (beliefs) padrão do agente
    agent.beliefs = {
        'received_attack': None, # Padrão: não foi atacado
        'target': None,          # Padrão: sem alvo
        'range': 1               # Padrão: range 1
    }
    
    # 4. Configurar mocks de atributos/métodos
    agent.cell = mocker.MagicMock()
    agent.cell.coordinate = (0, 0) # Posição padrão do agente
    
    # 5. Disponibilizar os mocks para os testes poderem configurá-los
    agent.MOCKS = {
        'target': mock_target
    }

    return agent


def test_intention_continuar(mock_retaliate_agent):
    """
    Caminho: Não (cond_foi_atacado)
    """
    agent = mock_retaliate_agent
    agent.beliefs['received_attack'] = None 
    
    logic_tree = RetaliateAttackPlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "CONTINUAR"


def test_intention_definir_alvo(mock_retaliate_agent):
    """
    Caminho: Sim (cond_foi_atacado) -> Não (cond_possui_alvo)
    """
    agent = mock_retaliate_agent
    agent.beliefs['received_attack'] = 123  
    agent.beliefs['target'] = None          
    
    logic_tree = RetaliateAttackPlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "DEFINIR ALVO"


def test_intention_atacar(mock_retaliate_agent):
    """
    Caminho: Sim (cond_foi_atacado) -> Sim (cond_possui_alvo) -> Sim (cond_consegue_atacar)
    """
    agent = mock_retaliate_agent
    mock_target = agent.MOCKS['target']
    
    agent.beliefs['received_attack'] = 123
    agent.beliefs['target'] = mock_target
    agent.beliefs['range'] = 1
    
    agent.cell.coordinate = (0, 0)
    mock_target.cell.coordinate = (0, 3) 
    
    logic_tree = RetaliateAttackPlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "ATACAR"


def test_intention_aproximar_se(mock_retaliate_agent):
    """
    Caminho: Sim (cond_foi_atacado) -> Sim (cond_possui_alvo) -> Não (cond_consegue_atacar)
    """
    agent = mock_retaliate_agent
    mock_target = agent.MOCKS['target']
    
    agent.beliefs['received_attack'] = 123
    agent.beliefs['target'] = mock_target
    agent.beliefs['range'] = 1
    
    agent.cell.coordinate = (0, 0)
    mock_target.cell.coordinate = (0, 4) 
    
    logic_tree = RetaliateAttackPlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "APROXIMAR-SE"


def test_coverage_agente_sem_celula_leva_a_aproximar_se(mock_retaliate_agent):
    """
    Testa o caminho: Sim (atacado) -> Sim (alvo) -> Não (consegue_atacar, pois agent.cell é None)
    """
    agent = mock_retaliate_agent
    mock_target = agent.MOCKS['target']
    
    agent.beliefs['received_attack'] = 123
    agent.beliefs['target'] = mock_target
    agent.cell = None # <-- Aciona a linha 31
    
    logic_tree = RetaliateAttackPlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "APROXIMAR-SE"


def test_coverage_target_sem_celula_leva_a_aproximar_se(mock_retaliate_agent):
    """
    Testa o caminho: Sim (atacado) -> Sim (alvo) -> Não (consegue_atacar, pois target.cell é None)
    """
    agent = mock_retaliate_agent
    mock_target = agent.MOCKS['target']
    
    agent.beliefs['received_attack'] = 123
    agent.beliefs['target'] = mock_target
    mock_target.cell = None 
    
    logic_tree = RetaliateAttackPlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "APROXIMAR-SE"


def test_coverage_get_distance_falha_leva_a_aproximar_se(mocker, mock_retaliate_agent):
    """
    Testa o caminho: Sim (atacado) -> Sim (alvo) -> Não (consegue_atacar, pois get_distance retorna None)
    """
    agent = mock_retaliate_agent
    mock_target = agent.MOCKS['target']
    
    agent.beliefs['received_attack'] = 123
    agent.beliefs['target'] = mock_target
    
    mocker.patch('BDIPlanLogic.RetaliateAttackPlanLogic.get_distance', return_value=None) #

    logic_tree = RetaliateAttackPlanLogic()
    intention = logic_tree.get_intention(agent)

    assert intention == "APROXIMAR-SE"