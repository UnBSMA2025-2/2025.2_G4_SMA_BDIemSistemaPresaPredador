import pytest
from unittest.mock import MagicMock, patch, call
from Agents.character_agent import Character_Agent

@pytest.fixture
def mock_agent_com_ambiente(mocker):
    """
    Cria um mock de Character_Agent e seu ambiente MESA.
    Inclui mocks para 'model', 'grid', e 'cell'.
    """
    # O spec=Character_Agent é usando para que o mock falhe se tentarmos
    # acessar um método ou atributo que não existe na classe real.
    agent = mocker.MagicMock(spec=Character_Agent)

    # --- Configuração do Ambiente Mockado ---
    agent.model = mocker.MagicMock()
    agent.model.grid = mocker.MagicMock()
    agent.model.steps = 10 # Um valor de tempo de simulação para o teste

    # O grid tem altura e largura
    agent.model.grid.height = 50
    agent.model.grid.width = 50

    # A célula atual do agente
    agent.cell = mocker.MagicMock()
    agent.cell.coordinate = (10, 10) # Posição inicial do agente

    # O dicionário de células visitadas deve ser real para testarmos
    agent.visited_cells = {}

    # --- Configuração da Célula de Destino Mockada ---
    mock_new_cell = mocker.MagicMock()
    mock_new_cell.coordinate = (15, 15) # Posição de destino
    mock_new_cell.is_empty = True # Por padrão, a célula de destino está vazia

    # Isso é crucial: mockamos a busca na grid do MESA.
    # self.model.grid.all_cells.select(...) deve retornar a célula que queremos.
    # O .select() retorna um objeto iterável (como uma lista).
    mock_selection = mocker.MagicMock()
    mock_selection.__iter__.return_value = [mock_new_cell]
    agent.model.grid.all_cells.select.return_value = mock_selection
    
    # Disponibilizar mocks internos para os testes
    agent.MOCKS = {
        'new_cell': mock_new_cell
    }
    
    return agent


@patch('Agents.character_agent.move_to_agent')
def test_move_to_target_quando_celula_esta_vazia(mock_move_to_agent, mock_agent_com_ambiente):
    """
    Testa o "caminho feliz": o agente se move para uma célula vazia.
    """
    agent = mock_agent_com_ambiente
    mock_new_cell = agent.MOCKS['new_cell']
    
    target_pos = (20, 20)
    new_pos_calculada = (15, 15)
    mock_move_to_agent.return_value = new_pos_calculada

    mock_new_cell.is_empty = True

    Character_Agent.move_to_target(agent, target_pos, 5)

    mock_move_to_agent.assert_called_once_with(
        h=50, l=50,
        ax=10, ay=10,
        bx=20, by=20,
        max_step=5
    )

    assert agent.cell == mock_new_cell

    assert agent.visited_cells[new_pos_calculada] == agent.model.steps
    assert (15, 15) in agent.visited_cells


@patch('Agents.character_agent.move_to_agent')
def test_move_to_target_quando_celula_esta_ocupada(mock_move_to_agent, mock_agent_com_ambiente):
    """
    Testa o "caminho triste": o agente tenta se mover, mas a célula de destino está ocupada.
    """
    agent = mock_agent_com_ambiente
    mock_new_cell = agent.MOCKS['new_cell']
    
    original_cell = agent.cell 
    
    target_pos = (20, 20)
    new_pos_calculada = (15, 15)
    mock_move_to_agent.return_value = new_pos_calculada
    
    mock_new_cell.is_empty = False

    Character_Agent.move_to_target(agent, target_pos, 5)

    assert agent.cell == original_cell
    assert agent.cell != mock_new_cell
    
    assert new_pos_calculada not in agent.visited_cells
    assert len(agent.visited_cells) == 0


@pytest.fixture
def mock_action_agent(mocker):
    """
    Cria um mock de Character_Agent com métodos-chave (como get_friends
    e move_to_target) já mockados para testes de ação.
    """
    agent = mocker.MagicMock(spec=Character_Agent)

    agent.beliefs = {
        'hp': 50,
        'num_healing': 2,
        'em_batalha': False,
        'displacement': 5
    }

    agent.cell = mocker.MagicMock()
    agent.unique_id = 'agent_test_01'
    
    agent.get_friends = mocker.MagicMock(return_value=[])
    agent.move_to_target = mocker.MagicMock()
    
    return agent


def test_heal_com_itens(mocker, mock_action_agent):
    """
    Caminho: Agente tem curas (num_healing > 0).
    Verifica se o HP aumenta e o número de curas diminui.
    """
    agent = mock_action_agent
    agent.beliefs['hp'] = 10
    agent.beliefs['num_healing'] = 2
    
    mocker.patch('Agents.character_agent.random.randint', return_value=3)

    Character_Agent.heal(agent)

    assert agent.beliefs['hp'] == 13 # 10 + 3
    assert agent.beliefs['num_healing'] == 1 # 2 - 1


def test_heal_sem_itens(mocker, mock_action_agent):
    """
    Caminho: Agente não tem curas (num_healing = 0).
    Verifica se nada acontece.
    """
    agent = mock_action_agent
    agent.beliefs['hp'] = 10
    agent.beliefs['num_healing'] = 0 #
    
    mock_randint = mocker.patch('Agents.character_agent.random.randint')

    Character_Agent.heal(agent)

    assert agent.beliefs['hp'] == 10
    assert agent.beliefs['num_healing'] == 0
    mock_randint.assert_not_called()


@pytest.fixture
def mock_friend_cell(mocker):
    """
    Cria um amigo mockado para todos os cenários
    (heal, target, etc.).
    """
    mock_friend = mocker.MagicMock()
    mock_friend.unique_id = 'friend_01'
    mock_friend.type = 'CHARACTER' #
    mock_friend.beliefs = {
        'em_batalha': False, 
        'target': None,
        'num_healing': 2  
    }
    mock_friend.inbox = [] 
    
    cell = mocker.MagicMock()
    cell.is_empty = False
    cell.agents = [mock_friend]
    return cell


def test_request_heal_com_amigo_disponivel(mock_action_agent, mock_friend_cell):
    """
    Caminho: Agente encontra um amigo que não está em batalha e tem curas.
    """
    agent = mock_action_agent
    agent.get_friends.return_value = [mock_friend_cell] 
    
    mock_friend = mock_friend_cell.agents[0]
    
    Character_Agent.request_heal(agent)

    assert len(mock_friend.inbox) == 1
    message = mock_friend.inbox[0]
    assert message['performative'] == 'SEND_HEALING'
    assert message['sender'] == agent.unique_id 
    assert message['receiver'] == mock_friend.unique_id 


def test_request_heal_amigo_em_batalha(mock_action_agent, mock_friend_cell):
    """
    Caminho: Amigo é encontrado, mas está em batalha.
    """
    agent = mock_action_agent
    mock_friend = mock_friend_cell.agents[0]
    mock_friend.beliefs['em_batalha'] = True 
    
    agent.get_friends.return_value = [mock_friend_cell]

    Character_Agent.request_heal(agent)

    assert len(mock_friend.inbox) == 0


def test_request_heal_amigo_sem_cura(mock_action_agent, mock_friend_cell):
    """
    Caminho: Amigo é encontrado, mas não tem curas suficientes.
    """
    agent = mock_action_agent
    mock_friend = mock_friend_cell.agents[0]
    mock_friend.beliefs['num_healing'] = 1 
    
    agent.get_friends.return_value = [mock_friend_cell]

    Character_Agent.request_heal(agent)

    assert len(mock_friend.inbox) == 0


def test_request_heal_sem_amigos(mock_action_agent):
    """
    Caminho: Agente não encontra amigos (get_friends retorna []).
    """
    agent = mock_action_agent
    agent.get_friends.return_value = [] #

    Character_Agent.request_heal(agent)

    agent.get_friends.assert_called_once()
    

def test_escape_chama_move_to_target_corretamente(mock_action_agent):
    """
    Verifica se 'escape' chama 'move_to_target' com os parâmetros corretos.
    """
    agent = mock_action_agent
    
    mock_vizinho_cell = MagicMock()
    mock_vizinho_cell.coordinate = (10, 11) 
    
    agent.cell.neighborhood.select_random_cell.return_value = mock_vizinho_cell #

    Character_Agent.escape(agent)

    agent.move_to_target.assert_called_once_with(
        (10, 11), 
        1)
    

@pytest.fixture
def mock_agent_base(mocker):
    """
    Um fixture base que fornece apenas o agente, pronto para
    ter seu ambiente (células, etc.) configurado por outros fixtures.
    """
    agent = mocker.MagicMock(spec=Character_Agent)
    
    agent.model = mocker.MagicMock()
    agent.model.grid = mocker.MagicMock()

    agent.beliefs = {
        'displacement': 5,
        'target': None,
        'em_batalha': False
    }
    agent.cell = mocker.MagicMock()

    agent.cell.neighborhood.cells = []
    agent.cell.get_neighborhood.return_value.cells = []
    return agent


@pytest.fixture
def mock_enemy_cell(mocker):
    """Cria uma célula mockada contendo um agente inimigo."""
    mock_enemy = mocker.MagicMock()
    mock_enemy.type = 'ANIMAL' 
    
    cell = mocker.MagicMock()
    cell.is_empty = False
    cell.agents = [mock_enemy]
    return cell


@pytest.fixture
def mock_friend_in_battle_cell(mocker):
    """Cria uma célula mockada contendo um amigo EM BATALHA."""
    mock_target_do_amigo = mocker.MagicMock() 
    
    mock_friend = mocker.MagicMock()
    mock_friend.type = 'CHARACTER'
    mock_friend.beliefs = {
        'em_batalha': True, 
        'target': mock_target_do_amigo 
    }
    
    cell = mocker.MagicMock()
    cell.is_empty = False
    cell.agents = [mock_friend]
    return cell


@pytest.fixture
def mock_empty_cell(mocker):
    """Cria uma célula mockada vazia."""
    cell = mocker.MagicMock()
    cell.is_empty = True 
    cell.agents = []
    return cell


def test_get_friends_encontra_amigo(mock_agent_base, mock_friend_cell, mock_enemy_cell):
    """
    Caminho: Um amigo e um inimigo estão no raio de "displacement".
    Verifica se apenas o amigo (CHARACTER) é retornado.
    """
    agent = mock_agent_base
    vizinhos = [mock_friend_cell, mock_enemy_cell]
    agent.cell.get_neighborhood.return_value.select.return_value.cells = [mock_friend_cell] #

    friend_cells = Character_Agent.get_friends(agent)

    assert friend_cells == [mock_friend_cell]
    call_args = agent.cell.get_neighborhood.return_value.select.call_args
    lambda_func = call_args[0][0] 
    
    assert lambda_func(mock_friend_cell) == True # Amigo (not empty, type='CHARACTER')
    assert lambda_func(mock_enemy_cell) == False # Inimigo (not empty, type!='CHARACTER')


def test_get_friends_nao_encontra_amigo(mock_agent_base):
    """
    Caminho: Apenas inimigos ou células vazias estão no raio.
    """
    agent = mock_agent_base
    agent.cell.get_neighborhood.return_value.select.return_value.cells = [] 

    friend_cells = Character_Agent.get_friends(agent)

    assert friend_cells == []


def test_set_target_encontra_inimigo_adjacente(mock_agent_base, mock_enemy_cell, mock_friend_cell):
    """
    Caminho: Um inimigo está em uma célula adjacente.
    """
    agent = mock_agent_base
    agent.cell.neighborhood.cells = [mock_friend_cell, mock_enemy_cell] #
    
    Character_Agent.set_target(agent)

    assert agent.beliefs['target'] == mock_enemy_cell.agents[0]
    assert agent.beliefs['em_batalha'] is True


def test_set_target_apenas_amigos_adjacentes(mock_agent_base, mock_friend_cell):
    """
    Caminho: Apenas amigos estão em células adjacentes.
    """
    agent = mock_agent_base
    agent.cell.neighborhood.cells = [mock_friend_cell] #

    Character_Agent.set_target(agent)

    assert agent.beliefs['target'] is None
    assert agent.beliefs['em_batalha'] is False


def test_set_friends_target_encontra_amigo_em_batalha(mock_agent_base, mock_friend_in_battle_cell, mock_friend_cell):
    """
    Caminho: Encontra um amigo em batalha e copia seu alvo.
    """
    agent = mock_agent_base
    amigo_em_batalha = mock_friend_in_battle_cell.agents[0]
    
    agent.cell.get_neighborhood.return_value.cells = [mock_friend_cell, mock_friend_in_battle_cell] #

    Character_Agent.set_friends_target(agent)

    assert agent.beliefs['target'] == amigo_em_batalha.beliefs['target']
    assert agent.beliefs['em_batalha'] is True


def test_set_friends_target_amigo_nao_esta_em_batalha(mock_agent_base, mock_friend_cell):
    """
    Caminho: Encontra um amigo, mas ele não está em batalha.
    """
    agent = mock_agent_base
    agent.cell.get_neighborhood.return_value.cells = [mock_friend_cell] #

    Character_Agent.set_friends_target(agent)

    assert agent.beliefs['target'] is None
    assert agent.beliefs['em_batalha'] is False


def test_set_friends_target_apenas_inimigos_perto(mock_agent_base, mock_enemy_cell):
    """
    Caminho: Apenas inimigos estão no raio de "displacement".
    """
    agent = mock_agent_base
    agent.cell.get_neighborhood.return_value.cells = [mock_enemy_cell] #

    Character_Agent.set_friends_target(agent)

    assert agent.beliefs['target'] is None
    assert agent.beliefs['em_batalha'] is False


def test_set_other_target_encontra_inimigo_mais_proximo(mock_agent_base, mock_enemy_cell, mock_empty_cell, mocker):
    """
    Caminho: Um inimigo é encontrado no raio 2 (o mais próximo).
    Verifica se o agente para de procurar e define o alvo corretamente.
    """
    agent = mock_agent_base
    agent.model.grid.width = 10  
    
    mock_enemy_cell_distante = mocker.MagicMock()
    mock_enemy_cell_distante.agents = [mocker.MagicMock(type='ANIMAL')]

    def get_neighborhood_side_effect(radius):
        if radius == 1:
            return MagicMock(cells=[mock_empty_cell]) 
        if radius == 2:
            return MagicMock(cells=[mock_enemy_cell]) 
        if radius == 3:
            return MagicMock(cells=[mock_enemy_cell_distante])
        return MagicMock(cells=[])

    agent.cell.get_neighborhood.side_effect = get_neighborhood_side_effect

    Character_Agent.set_other_target(agent)

    assert agent.beliefs['target'] == mock_enemy_cell.agents[0] #
    assert agent.beliefs['em_batalha'] is True #
    
    assert agent.cell.get_neighborhood.call_count == 2
    agent.cell.get_neighborhood.assert_has_calls([call(1), call(2)])


def test_set_other_target_nao_encontra_inimigo(mock_agent_base, mock_empty_cell):
    """
    Caminho: Nenhum inimigo é encontrado em todo o grid.
    """
    agent = mock_agent_base
    agent.model.grid.width = 5 
    
    agent.cell.get_neighborhood.return_value = MagicMock(cells=[mock_empty_cell])

    Character_Agent.set_other_target(agent)

    assert agent.beliefs['target'] is None
    assert agent.beliefs['em_batalha'] is False
    
    assert agent.cell.get_neighborhood.call_count == 4
    agent.cell.get_neighborhood.assert_has_calls([call(1), call(2), call(3), call(4)])


def test_get_heal_recebe_cura(mock_agent_base):
    """
    Verifica se o número de curas do agente aumenta ao receber a mensagem.
    """
    agent = mock_agent_base
    agent.beliefs['num_healing'] = 1 
    
    message = {
        'content': {'num_healing': 2} 
    }
    
    Character_Agent.get_heal(agent, message)
    
    assert agent.beliefs['num_healing'] == 3 


def test_send_heal_envia_cura_para_requisitante(mock_agent_base):
    """
    Verifica se o agente envia uma mensagem de 'GET_HEALING'
    para o agente que pediu e gasta um item de cura.
    """
    agent = mock_agent_base
    agent.unique_id = 'agente_curandeiro'
    agent.beliefs['num_healing'] = 5 
    
    mock_receiver = MagicMock()
    mock_receiver.unique_id = 'agente_ferido'
    mock_receiver.inbox = [] 
    
    request_message = {
        'performative': 'SEND_HEALING',
        'sender': 'agente_ferido', 
        'conversation_id': 'convo_abc123' 
    }
    
    agent.model.get_agent_by_id.return_value = mock_receiver 

    Character_Agent.send_heal(agent, request_message)

    assert agent.beliefs['num_healing'] == 4 

    agent.model.get_agent_by_id.assert_called_once_with('agente_ferido')

    assert len(mock_receiver.inbox) == 1 
    response_message = mock_receiver.inbox[0]
    
    assert response_message['performative'] == 'GET_HEALING' 
    assert response_message['sender'] == 'agente_curandeiro'
    assert response_message['receiver'] == 'agente_ferido' 
    assert response_message['content'] == {'num_healing': 1} 
    assert response_message['conversation_id'] == 'convo_abc123' 


@pytest.fixture
def mock_combat_agents(mocker):
    """
    Cria um par de agentes mockados para testes de interação:
    'agent' (o agente em teste) e 'other_agent' (o alvo/atacante).
    """
    agent = mocker.MagicMock(spec=Character_Agent)
    agent.unique_id = 'agent_01'
    agent.beliefs = {
        'hp': 50,
        'def': 10,
        'atk': 15,
        'classe': 'GUERREIRO',
        'target': None,
        'em_batalha': False,
        'is_alive': True
    }
    agent.inbox = []
    agent.remove = mocker.MagicMock()

    other_agent = mocker.MagicMock(spec=Character_Agent)
    other_agent.unique_id = 'other_02'
    other_agent.beliefs = {
        'hp': 40,
        'target': None,
        'is_alive': True
    }
    other_agent.inbox = []

    agent.model = mocker.MagicMock()

    def get_agent_side_effect(agent_id):
        if agent_id == 'agent_01':
            return agent
        if agent_id == 'other_02':
            return other_agent
        return None
    
    agent.model.get_agent_by_id.side_effect = get_agent_side_effect
    
    return agent, other_agent


@patch('Agents.character_agent.uuid.uuid4', return_value='test-uuid')
@patch('Agents.character_agent.random.randint', return_value=5)
def test_attack_enemy_caminho_padrao(mock_randint, mock_uuid, mock_combat_agents):
    """
    Caminho: Agente (Guerreiro) ataca um alvo.
    """
    agent, other_agent = mock_combat_agents
    agent.beliefs['target'] = other_agent 
    agent.beliefs['em_batalha'] = False
    
    Character_Agent.attack_enemy(agent)

    assert agent.beliefs['em_batalha'] is True 
    
    assert len(other_agent.inbox) == 1 
    message = other_agent.inbox[0]
    
    assert message['performative'] == 'ATTACK_TARGET' 
    assert message['sender'] == 'agent_01' 
    assert message['receiver'] == 'other_02' 
    assert message['content']['atk'] == 15 
    assert message['conversation_id'] == 'test-uuid' 

    mock_randint.assert_not_called()


@patch('Agents.character_agent.uuid.uuid4', return_value='test-uuid')
@patch('Agents.character_agent.random.randint', return_value=5)
def test_attack_enemy_ladino_ataque_furtivo(mock_randint, mock_uuid, mock_combat_agents):
    """
    Caminho: Agente (LADINO) ataca um alvo que o está alvejando.
    """
    agent, other_agent = mock_combat_agents
    agent.beliefs['target'] = other_agent
    agent.beliefs['classe'] = 'LADINO' 
    other_agent.beliefs['target'] = agent 
    
    Character_Agent.attack_enemy(agent)

    mock_randint.assert_called_once_with(1, 16) 
    
    message = other_agent.inbox[0]
    assert message['content']['atk'] == 20


def test_attack_enemy_sem_alvo(mock_combat_agents):
    """
    Caminho: Agente tenta atacar, mas não tem alvo.
    """
    agent, other_agent = mock_combat_agents
    agent.beliefs['target'] = None 
    agent.beliefs['em_batalha'] = True 
    
    Character_Agent.attack_enemy(agent)
    
    assert agent.beliefs['em_batalha'] is False 
    assert len(other_agent.inbox) == 0


def test_receive_attack_dano_sobrevivivel(mock_combat_agents):
    """
    Caminho: Agente recebe um ataque, mas sobrevive.
    """
    agent, other_agent = mock_combat_agents
    agent.beliefs['hp'] = 50
    agent.beliefs['def'] = 10
    
    attack_message = {
        'performative': 'ATTACK_TARGET',
        'sender': 'other_02', 
        'content': {'atk': 25}, 
        'conversation_id': 'c1'
    }

    Character_Agent.receive_attack(agent, attack_message)

    assert agent.beliefs['hp'] == 35 
    assert agent.beliefs['is_alive'] is True 
    
    agent.remove.assert_not_called()
    
    assert len(other_agent.inbox) == 1 
    response = other_agent.inbox[0]
    assert response['performative'] == 'ATTACK_RESPONSE' 
    assert response['content']['is_alive'] is True 


def test_receive_attack_dano_letal(mock_combat_agents):
    """
    Caminho: Agente recebe um ataque e morre.
    """
    agent, other_agent = mock_combat_agents
    agent.beliefs['hp'] = 20
    agent.beliefs['def'] = 10
    
    attack_message = {
        'performative': 'ATTACK_TARGET',
        'sender': 'other_02',
        'content': {'atk': 50}, 
        'conversation_id': 'c1'
    }
    
    Character_Agent.receive_attack(agent, attack_message)

    assert agent.beliefs['hp'] == 0 
    assert agent.beliefs['is_alive'] is False 
    
    agent.remove.assert_called_once() 
    
    assert len(other_agent.inbox) == 1
    assert other_agent.inbox[0]['content']['is_alive'] is False 


def test_receive_attack_dano_zero_defesa_alta(mock_combat_agents):
    """
    Caminho: Agente recebe um ataque, mas a defesa bloqueia todo o dano.
    """
    agent, other_agent = mock_combat_agents
    agent.beliefs['hp'] = 50
    agent.beliefs['def'] = 30
    
    attack_message = {'content': {'atk': 25}, 'sender': 'other_02', 'conversation_id': 'c1'} 
    
    Character_Agent.receive_attack(agent, attack_message)

    assert agent.beliefs['hp'] == 50 
    assert agent.beliefs['is_alive'] is True
    agent.remove.assert_not_called()
    assert len(other_agent.inbox) == 1 


def test_attack_response_alvo_morreu(mock_combat_agents):
    """
    Caminho: Agente recebe a resposta de que seu alvo morreu.
    """
    agent, other_agent = mock_combat_agents
    agent.beliefs['target'] = other_agent 
    agent.beliefs['em_batalha'] = True
    
    response_message = {'content': {'is_alive': False}} 
    
    Character_Agent.attack_response(agent, response_message)
    
    assert agent.beliefs['target'] is None 
    assert agent.beliefs['em_batalha'] is False 


def test_attack_response_alvo_sobreviveu(mock_combat_agents):
    """
    Caminho: Agente recebe a resposta de que seu alvo sobreviveu.
    """
    agent, other_agent = mock_combat_agents
    agent.beliefs['target'] = other_agent
    agent.beliefs['em_batalha'] = True
    
    response_message = {'content': {'is_alive': True}} 
    
    Character_Agent.attack_response(agent, response_message)
    
    assert agent.beliefs['target'] == other_agent
    assert agent.beliefs['em_batalha'] is True


@pytest.fixture
def mock_exploration_agent(mocker):
    """
    Cria um mock de Character_Agent com mocks detalhados para
    o ambiente de exploração (células, vizinhança, etc.).
    """
    agent = mocker.MagicMock(spec=Character_Agent)

    agent.model = mocker.MagicMock()
    agent.model.steps = 100 
    
    agent.cell = mocker.MagicMock()
    agent.cell.neighborhood = mocker.MagicMock()

    mock_cell_A = mocker.MagicMock(coordinate=(1, 1), is_empty=True)
    mock_cell_B = mocker.MagicMock(coordinate=(1, 2), is_empty=True)
    mock_cell_C = mocker.MagicMock(coordinate=(1, 3), is_empty=False) 
    
    agent.cell.neighborhood.cells = [mock_cell_A, mock_cell_B, mock_cell_C]

    agent.visited_cells = {} 
    agent.exploration_cooldown = 70 #
    
    agent.random = mocker.MagicMock()

    agent.MOCKS = {
        'cell_A': mock_cell_A,
        'cell_B': mock_cell_B,
        'cell_C': mock_cell_C
    }
    return agent


def test_select_smart_exploration_sem_vizinhos_vazios(mock_exploration_agent):
    """
    Caminho 1: Não há vizinhos vazios disponíveis.
    """
    agent = mock_exploration_agent

    agent.MOCKS['cell_A'].is_empty = False
    agent.MOCKS['cell_B'].is_empty = False
    agent.cell.neighborhood.cells = [
        agent.MOCKS['cell_A'], agent.MOCKS['cell_B'], agent.MOCKS['cell_C']
    ]

    result = Character_Agent._select_smart_exploration_cell(agent)

    assert result is None #


def test_select_smart_exploration_prefere_nao_visitadas(mock_exploration_agent):
    """
    Caminho 2: Há células vazias, e uma delas nunca foi visitada.
    """
    agent = mock_exploration_agent
    
    agent.visited_cells = { (1, 2): 50 } 
    
    agent.cell.neighborhood.cells = [agent.MOCKS['cell_A'], agent.MOCKS['cell_B']]
    
    agent.random.choice.return_value = agent.MOCKS['cell_A']

    result = Character_Agent._select_smart_exploration_cell(agent)

    assert result == agent.MOCKS['cell_A']
    
    agent.random.choice.assert_called_once_with([agent.MOCKS['cell_A']])


def test_select_smart_exploration_prefere_visitada_ha_mais_tempo(mock_exploration_agent):
    """
    Caminho 3: Todas as células vazias foram visitadas.
    Deve escolher a que foi visitada há mais tempo (e passou do cooldown).
    """
    agent = mock_exploration_agent
    agent.model.steps = 100
    agent.exploration_cooldown = 70 #
    
    agent.visited_cells = { (1, 1): 50, (1, 2): 10 }
    
    agent.cell.neighborhood.cells = [agent.MOCKS['cell_A'], agent.MOCKS['cell_B']]
    
    result = Character_Agent._select_smart_exploration_cell(agent)

    assert result == agent.MOCKS['cell_B']
    agent.random.choice.assert_not_called()


def test_select_smart_exploration_fallback_para_aleatorio_recente(mock_exploration_agent):
    """
    Caminho 4: Todas as células vazias foram visitadas,
    mas NENHUMA passou do cooldown.
    """
    agent = mock_exploration_agent
    agent.model.steps = 100
    agent.exploration_cooldown = 70 #
    
    agent.visited_cells = { (1, 1): 50, (1, 2): 40 } 
    
    agent.cell.neighborhood.cells = [agent.MOCKS['cell_A'], agent.MOCKS['cell_B']]
    
    agent.random.choice.return_value = agent.MOCKS['cell_B']

    result = Character_Agent._select_smart_exploration_cell(agent)

    assert result == agent.MOCKS['cell_B']
    
    agent.random.choice.assert_called_once_with(
        [agent.MOCKS['cell_A'], agent.MOCKS['cell_B']]
    )


def test_deliberate_seleciona_plano_correto_do_desejo(mocker):
    """
    Verifica se o método 'deliberate' usa o desejo atual
    para selecionar o plano correto da 'plan_library'.
    """
    agent = mocker.MagicMock(spec=Character_Agent)
    
    mock_survive_plan = mocker.MagicMock()
    mock_battle_plan = mocker.MagicMock()
    mock_explore_plan = mocker.MagicMock()
    
    mock_survive_plan.get_intention.return_value = "INTENCAO_SOBREVIVER"
    mock_battle_plan.get_intention.return_value = "INTENCAO_BATALHAR"
    mock_explore_plan.get_intention.return_value = "INTENCAO_EXPLORAR"

    agent.plan_library = {
        'SURVIVE': mock_survive_plan,
        'BATTLE': mock_battle_plan,
        'EXPLORE': mock_explore_plan,
    }
    
    agent.desires = ['BATTLE']

    Character_Agent.deliberate(agent)

    assert agent.intention == "INTENCAO_BATALHAR" #
    
    mock_battle_plan.get_intention.assert_called_once_with(agent)
    
    mock_survive_plan.get_intention.assert_not_called()
    mock_explore_plan.get_intention.assert_not_called()


@pytest.fixture
def mock_execute_agent(mocker):
    """
    Cria um mock de Character_Agent com TODOS os seus métodos de ação
    (heal, attack_enemy, etc.) mockados como espiões.
    
    Isso nos permite verificar qual método é chamado por 'execute_plan'.
    """
    agent = mocker.MagicMock(spec=Character_Agent)

    agent.heal = mocker.MagicMock()
    agent.attack_enemy = mocker.MagicMock()
    agent.move_to_target = mocker.MagicMock()
    agent.escape = mocker.MagicMock()
    agent.request_heal = mocker.MagicMock()
    agent.set_target = mocker.MagicMock()
    agent.set_friends_target = mocker.MagicMock()
    agent.set_other_target = mocker.MagicMock()
    agent.unique_id = 'mock_exec_agent'
    
    agent.get_friends = mocker.MagicMock(return_value=[])
    agent._select_smart_exploration_cell = mocker.MagicMock(return_value=None)
    
    agent.beliefs = {
        'target': None,
        'displacement': 5,
        'healing_item_spot': (10, 10),
        'num_healing': 1
    }
    agent.cell = mocker.MagicMock()
    agent.cell.beliefs = {}
    agent.cell.coordinate = (0, 0)
    
    agent.model = mocker.MagicMock()
    agent.model.healing_layer = mocker.MagicMock()
    agent.model.healing_layer.data = {} 
    
    return agent


@pytest.mark.parametrize("intention_name, expected_method_to_call", [
    ('CURAR', 'heal'),
    ('ATACAR INIMIGO', 'attack_enemy'),
    ('FUGIR', 'escape'),
    ('OBTER CURA', 'request_heal'),
    ('DEFINIR ALVO', 'set_target'),
    ('DEFINIR ALVO DO AMIGO', 'set_friends_target'),
    ('DEFINIR OUTRO ALVO', 'set_other_target'),
])
def test_execute_plan_simple_dispatch(mock_execute_agent, intention_name, expected_method_to_call):
    """
    Testa se a intenção X chama o método de ação Y.
    """
    agent = mock_execute_agent
    agent.intention = intention_name 
    
    method_to_check = getattr(agent, expected_method_to_call)

    Character_Agent.execute_plan(agent)

    method_to_check.assert_called_once()


@pytest.mark.parametrize("intention_name", ['ESPERAR', 'INTENCAO_INVALIDA', None])
def test_execute_plan_do_nothing_cases(mock_execute_agent, intention_name):
    """
    Testa os casos 'ESPERAR' e o default ('_'),
    que não devem chamar nenhuma ação.
    """
    agent = mock_execute_agent
    agent.intention = intention_name

    Character_Agent.execute_plan(agent)

    agent.heal.assert_not_called()
    agent.attack_enemy.assert_not_called()
    agent.move_to_target.assert_not_called()
    agent.escape.assert_not_called()
    agent.request_heal.assert_not_called()
    agent.set_target.assert_not_called()
    agent.set_friends_target.assert_not_called()
    agent.set_other_target.assert_not_called()


def test_execute_plan_aproximar_se_com_alvo(mock_execute_agent):
    """
    Testa o 'case APROXIMAR-SE' quando o alvo existe.
    """
    agent = mock_execute_agent
    agent.intention = 'APROXIMAR-SE'
    
    mock_target = MagicMock()
    mock_target.cell.coordinate = (5, 5)
    agent.beliefs['target'] = mock_target
    agent.beliefs['displacement'] = 3
    
    Character_Agent.execute_plan(agent)
    
    agent.move_to_target.assert_called_once_with((5, 5), 3)


def test_execute_plan_aproximar_se_sem_alvo(mock_execute_agent):
    """
    Testa o 'case APROXIMAR-SE' quando o alvo é None.
    """
    agent = mock_execute_agent
    agent.intention = 'APROXIMAR-SE'
    agent.beliefs['target'] = None 
    
    Character_Agent.execute_plan(agent)
    
    agent.move_to_target.assert_not_called()


def test_execute_plan_aproximar_de_amigo(mock_execute_agent, mocker):
    """
    Testa o 'case APROXIMAR-SE DE AMIGO'
    """
    agent = mock_execute_agent
    agent.intention = 'APROXIMAR-SE DE AMIGO'
    
    mock_friend_agent = mocker.MagicMock()
    mock_friend_agent.beliefs = {'em_batalha': False} 
    mock_friend_agent.cell.coordinate = (8, 8)
    
    mock_friend_cell = mocker.MagicMock()
    mock_friend_cell.agents = [mock_friend_agent]
    
    agent.get_friends.return_value = [mock_friend_cell]
    agent.beliefs['displacement'] = 5

    Character_Agent.execute_plan(agent)
    
    agent.move_to_target.assert_called_once_with((8, 8), 5) 


def test_execute_plan_explorar_celula_encontrada(mock_execute_agent, mocker):
    """
    Testa o 'case EXPLORAR' quando uma célula é encontrada.
    """
    agent = mock_execute_agent
    agent.intention = 'EXPLORAR'
    
    mock_best_cell = mocker.MagicMock()
    mock_best_cell.coordinate = (1, 2)
    
    agent._select_smart_exploration_cell.return_value = mock_best_cell 
    agent.beliefs['displacement'] = 5
    
    Character_Agent.execute_plan(agent)
    
    agent._select_smart_exploration_cell.assert_called_once()
    agent.move_to_target.assert_called_once_with((1, 2), 5) 


def test_execute_plan_explorar_sem_celula(mock_execute_agent):
    """
    Testa o 'case EXPLORAR' quando está preso (else).
    """
    agent = mock_execute_agent
    agent.intention = 'EXPLORAR'
    
    agent._select_smart_exploration_cell.return_value = None
    
    Character_Agent.execute_plan(agent)
    
    agent._select_smart_exploration_cell.assert_called_once()
    agent.move_to_target.assert_not_called()


def test_execute_plan_aproximar_do_item(mock_execute_agent):
    """
    Testa o 'case APROXIMAR DO ITEM'.
    """
    agent = mock_execute_agent
    agent.intention = 'APROXIMAR DO ITEM'
    
    agent.beliefs['healing_item_spot'] = (7, 7) 
    agent.beliefs['displacement'] = 5
    
    Character_Agent.execute_plan(agent)
    
    agent.move_to_target.assert_called_once_with((7, 7), 5)


def test_execute_plan_adquirir_item(mock_execute_agent):
    """
    Testa o 'case ADQUIRIR ITEM'.
    """
    agent = mock_execute_agent
    agent.intention = 'ADQUIRIR ITEM'
    
    agent.beliefs['num_healing'] = 1
    agent.beliefs['healing_item_spot'] = (5, 5) 
    
    agent.cell.beliefs = {'healing_item_spot': True} 
    agent.cell.coordinate = (5, 5)
    
    agent.model.healing_layer.data = {(5, 5): 1}
    
    Character_Agent.execute_plan(agent)
    
    assert agent.beliefs['num_healing'] == 2 
    assert agent.cell.beliefs['healing_item_spot'] is False 
    assert agent.beliefs['healing_item_spot'] is None 
    assert agent.model.healing_layer.data[(5, 5)] == 0 


def test_execute_plan_adquirir_item_falha(mock_execute_agent):
    """
    Testa o 'case ADQUIRIR ITEM' quando o 'if' falha.
    """
    agent = mock_execute_agent
    agent.intention = 'ADQUIRIR ITEM'
    
    agent.beliefs['num_healing'] = 1
    agent.cell.beliefs = {'healing_item_spot': False} 
    
    Character_Agent.execute_plan(agent)
    
    assert agent.beliefs['num_healing'] == 1


@pytest.fixture
def mock_messaging_agent(mocker):
    """
    Cria um mock de Character_Agent com métodos de processamento
    de mensagens mockados como 'espiões'.
    """
    agent = mocker.MagicMock(spec=Character_Agent)
    
    agent.inbox = [] 
    
    agent.send_heal = mocker.MagicMock()
    agent.get_heal = mocker.MagicMock()
    agent.receive_attack = mocker.MagicMock()
    agent.attack_response = mocker.MagicMock()
    
    return agent


@pytest.mark.parametrize("performative, expected_method_to_call", [
    ('SEND_HEALING', 'send_heal'),         
    ('GET_HEALING', 'get_heal'),           
    ('ATTACK_TARGET', 'receive_attack'),   
    ('ATTACK_RESPONSE', 'attack_response'),
])
def test_process_message_dispatches_para_metodo_correto(mock_messaging_agent, performative, expected_method_to_call):
    """
    Testa se o 'match' chama o método correto baseado no 'performative'.
    """
    agent = mock_messaging_agent
    
    test_message = {'performative': performative, 'content': 'dados_teste'}
    agent.inbox = [test_message] 
    
    spy_method = getattr(agent, expected_method_to_call)

    Character_Agent.process_message(agent)

    spy_method.assert_called_once_with(test_message)
    
    assert len(agent.inbox) == 0 

def test_process_message_lida_com_multiplas_mensagens(mock_messaging_agent):
    """
    Testa se o loop 'for' processa todas as mensagens na inbox.
    """
    agent = mock_messaging_agent
    
    msg1 = {'performative': 'ATTACK_TARGET', 'id': 1}
    msg2 = {'performative': 'SEND_HEALING', 'id': 2}
    
    agent.inbox = [msg1, msg2]

    Character_Agent.process_message(agent)

    agent.receive_attack.assert_called_once_with(msg1)
    agent.send_heal.assert_called_once_with(msg2)
    
    assert len(agent.inbox) == 0

def test_process_message_ignora_performative_desconhecido(mock_messaging_agent):
    """
    Testa se a mensagem é removida mesmo se o 'performative' não for
    reconhecido (o 'case _' padrão do 'match').
    """
    agent = mock_messaging_agent
    
    msg_invalid = {'performative': 'FAZER_CAFE', 'id': 1}
    agent.inbox = [msg_invalid]

    Character_Agent.process_message(agent)

    agent.send_heal.assert_not_called()
    agent.get_heal.assert_not_called()
    agent.receive_attack.assert_not_called()
    agent.attack_response.assert_not_called()
    
    assert len(agent.inbox) == 0 

    