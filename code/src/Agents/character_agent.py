from Interfaces.IBDI_Agent import IBDI_Agent
from utils.move_to_agent import move_to_agent
from BDIPlanLogic.SurvivePlanLogic import SurvivePlanLogic
from BDIPlanLogic.BattlePlanLogic import BattlePlanLogic
from BDIPlanLogic.ExplorationPlanLogic import ExplorationPlanLogic
from communication import MessageDict
from BDIPlanLogic.CharacterDesires import get_desire
import uuid
import random
import copy


class Character_Agent(IBDI_Agent):
    """
    Um agente que representa um personagem de RPG com lógica BDI.
    """
    def __init__(self, model, cell, beliefs, type='CHARACTER'):
        super().__init__(model)
        self.cell = cell
        self.type = type
        self.plan_library = {
            'SURVIVE': SurvivePlanLogic(),
            'BATTLE': BattlePlanLogic(),
            'EXPLORE': ExplorationPlanLogic(),
        }
        self.inbox = []
        self.beliefs = copy.deepcopy(beliefs)
        self.desires = ['']
        self.intention = None
        self.visited_cells = {}
        self.exploration_cooldown = 70

    # ---------------------- INTERAÇÃO ENTRE AGENTES ---------------------- #
    def get_friends(self):
        if self.cell is not None:
            vizinhos = self.cell.get_neighborhood(
                self.beliefs['displacement'])
            cell_agentes_amigos = vizinhos.select(
                lambda cell: not cell.is_empty and next(iter(cell.agents)).type == 'CHARACTER').cells
            return cell_agentes_amigos

    def move_to_target(self, target_coordinate, displacement):
        if not self.cell: self.explore()

        h = self.model.grid.height
        l = self.model.grid.width
        pos_a = self.cell.coordinate
        pos_b = target_coordinate

        new_position = move_to_agent(
            h=h,
            l=l,
            ax=pos_a[0],
            ay=pos_a[1],
            bx=pos_b[0],
            by=pos_b[1],
            max_step=displacement
        )

        new_cell = next(iter(self.model.grid.all_cells.select(
            lambda cell: cell.coordinate == new_position
        )))
        print(new_cell)

        if new_cell.is_empty:
            self.cell = new_cell
            self.visited_cells[new_cell.coordinate] = self.model.steps

    # ---------------------- EXPLORAÇÃO ---------------------- #
    def _select_smart_exploration_cell(self):
        neighbors = self.cell.neighborhood.cells
        empty_neighbors = [cell for cell in neighbors if cell.is_empty]

        if not empty_neighbors:
            return None

        unvisited_cells = [cell for cell in empty_neighbors if cell.coordinate not in self.visited_cells]
        if unvisited_cells:
            return self.random.choice(unvisited_cells)

        oldest_cell = None
        min_last_visit_step = -1

        for cell in empty_neighbors:
            last_visit_step = self.visited_cells.get(cell.coordinate, 0)
            if (self.model.steps - last_visit_step) > self.exploration_cooldown:
                if oldest_cell is None or last_visit_step < min_last_visit_step:
                    min_last_visit_step = last_visit_step
                    oldest_cell = cell

        if oldest_cell:
            return oldest_cell
        return self.random.choice(empty_neighbors)

    def explore(self):
        best_cell = self._select_smart_exploration_cell()
        if best_cell:
            # print(f'AGENTE [{self.unique_id}] explorando (inteligente) para: {best_cell.coordinate}')
            self.move_to_target(best_cell.coordinate, self.beliefs['displacement'])
        else:
            print(f'AGENTE [{self.unique_id}] está preso. Intenção: ESPERAR.')

    # ---------------------- COMBATE ---------------------- #
    def attack_enemy(self):
        enemyAgent = self.beliefs.get('target')

        if enemyAgent is None:
            self.beliefs['em_batalha'] = False
            return

        # ✅ Garante que o agente esteja em batalha
        self.beliefs['em_batalha'] = True

        if enemyAgent.beliefs.get('target') == self and self.beliefs['classe'] == 'LADINO':
            atk_valor = self.beliefs['atk'] + random.randint(1, 16)
        else:
            atk_valor = self.beliefs['atk']

        message = MessageDict(
            performative='ATTACK_TARGET',
            sender=self.unique_id,
            receiver=enemyAgent.unique_id,
            content={'atk': atk_valor},
            conversation_id=uuid.uuid4()
        )

        enemyAgent.inbox.append(message)

    def heal(self):
        if self.beliefs['num_healing'] > 0:
            self.beliefs['hp'] += random.randint(1, 4)
            self.beliefs['num_healing'] -= 1

    def request_heal(self):
        for cell in self.get_friends():
            if not cell.agents[0].beliefs['em_batalha'] and cell.agents[0].beliefs['num_healing'] > 1:
                message = MessageDict(
                    performative='SEND_HEALING',
                    sender=self.unique_id,
                    receiver=cell.agents[0].unique_id,
                    content={},
                    conversation_id=uuid.uuid4()
                )
                cell.agents[0].inbox.append(message)
                return

    def escape(self):
        if self.cell is not None:
            vizinho = self.cell.neighborhood.select_random_cell()
            self.move_to_target(vizinho.coordinate, 1)

    # ---------------------- DEFINIÇÃO DE ALVOS ---------------------- #
    def set_target(self):
        vizinhos = self.cell.get_neighborhood(self.beliefs['displacement']).cells
        for cell in vizinhos:
            if len(cell.agents) != 0 and cell.agents[0].type != 'CHARACTER':
                enemy_id = cell.agents[0].unique_id
                enemy = self.model.get_agent_by_id(enemy_id)
                self.beliefs['target'] = enemy
                self.beliefs['target'].cell = enemy.cell
                self.beliefs['em_batalha'] = True  # ✅ Entrou em batalha
                return

    def set_friends_target(self):
        vizinhos = self.cell.get_neighborhood(self.beliefs['displacement']).cells
        for cell in vizinhos:
            if len(cell.agents) != 0:
                friend = cell.agents[0]
                if friend.type == 'CHARACTER' and friend.beliefs['em_batalha']:
                    self.beliefs['target'] = friend.beliefs['target']
                    self.beliefs['em_batalha'] = True  # ✅ Segue o amigo em batalha
                    return

    def set_other_target(self):
        for i in range(1, self.model.grid.width):
            vizinhos = self.cell.get_neighborhood(i).cells
            for cell in vizinhos:
                if len(cell.agents) != 0 and cell.agents[0].type != 'CHARACTER':
                    self.beliefs['target'] = cell.agents[0]
                    self.beliefs['em_batalha'] = True  # ✅ Entrou em batalha
                    return

    # ---------------------- CURA VIA MENSAGENS ---------------------- #
    def get_heal(self, message):
        self.beliefs['num_healing'] += message['content']['num_healing']

    def send_heal(self, message):
        receiver = self.model.get_agent_by_id(message['sender'])
        response = MessageDict(
            performative='GET_HEALING',
            sender=self.unique_id,
            receiver=receiver.unique_id,
            content={'num_healing': 1},
            conversation_id=message['conversation_id']
        )
        receiver.inbox.append(response)
        self.beliefs['num_healing'] -= 1

    # ---------------------- RECEBER/RESPONDER ATAQUES ---------------------- #
    def receive_attack(self, message):
        damage = message['content']['atk'] - self.beliefs['def']
        newHp = self.beliefs['hp'] - max(0, damage)

        if newHp <= 0:
            self.beliefs['is_alive'] = False
            self.beliefs['hp'] = 0
        else:
            self.beliefs['hp'] = newHp

        response = MessageDict(
            performative='ATTACK_RESPONSE',
            sender=self.unique_id,
            receiver=message['sender'],
            content={'is_alive': self.beliefs['is_alive']},
            conversation_id=message['conversation_id'])
        receiver = self.model.get_agent_by_id(message['sender'])
        if receiver is not None:
            receiver.inbox.append(response)

        if not self.beliefs['is_alive']:
            self.remove()

    def attack_response(self, message):
        if not message['content']['is_alive']:
            self.beliefs['target'] = None
            self.beliefs['em_batalha'] = False  # ✅ Saiu da batalha
        return

    # ---------------------- CICLO BDI ---------------------- #
    def update_desires(self):
        self.desires[0] = get_desire(self)

    def deliberate(self):
        self.intention = self.plan_library[self.desires[0]].get_intention(self)

    def execute_plan(self):
        match self.intention:
            case 'CURAR':
                self.heal()
                return
            case 'ATACAR INIMIGO':
                self.attack_enemy()
                return
            case 'APROXIMAR-SE':
                print(f':\n----> {self.beliefs['target'].unique_id}')
                enemy = self.model.get_agent_by_id(self.beliefs['target'].unique_id)
                print(f'APROXIMAR-SE:\n----> {enemy}')
               
                if self.beliefs['target'] and self.beliefs['target'].cell:
                    self.move_to_target(
                        enemy.cell.coordinate,
                        self.beliefs['displacement'])
                return
            case 'FUGIR':
                self.escape()
                return
            case 'APROXIMAR-SE DE AMIGO':
                for cell in self.get_friends():
                    if not cell.agents[0].beliefs['em_batalha']:
                        friend_pos = cell.agents[0].cell.coordinate
                        self.move_to_target(friend_pos, self.beliefs['displacement'])
                        return
            case 'OBTER CURA':
                self.request_heal()
                return
            case 'DEFINIR ALVO':
                self.set_target()
                return
            case 'DEFINIR ALVO DO AMIGO':
                self.set_friends_target()
                return
            case 'DEFINIR OUTRO ALVO':
                self.set_other_target()
                return
            case 'EXPLORAR':
                self.explore()
                return
            case 'APROXIMAR DO ITEM':
                item_pos = self.beliefs['healing_item_spot']
                self.move_to_target(item_pos, self.beliefs['displacement'])
                return
            case 'ADQUIRIR ITEM':
                if self.cell.beliefs.get('healing_item_spot', False):
                    self.beliefs['num_healing'] += 1
                    self.cell.beliefs['healing_item_spot'] = False
                    self.beliefs['healing_item_spot'] = None
                    try:
                        healing_layer = self.model.healing_layer
                        pos = self.cell.coordinate
                        healing_layer.data[pos] = 0
                        # print(f"AGENTE [{self.unique_id}] adquiriu item em {pos}.")
                    except (KeyError, AttributeError) as e:
                        print(f"AVISO [{self.unique_id}]: Falha ao atualizar camada de cura. Erro: {e}")
                else:
                    print(f"AVISO [{self.unique_id}]: célula sem item de cura.")
                return
            case _:
                pass

    def process_message(self):
        for message in list(self.inbox):
            match message['performative']:
                case 'SEND_HEALING':
                    self.send_heal(message)
                case 'GET_HEALING':
                    self.get_heal(message)
                case 'ATTACK_TARGET':
                    self.receive_attack(message)
                case 'ATTACK_RESPONSE':
                    self.attack_response(message)
            self.inbox.remove(message)

    def step(self):
        print("-" * 40)
        print(f"Executando step do personagem...")
        print(f'INBOX: {self.inbox}')
        self.process_message()
        self.update_desires()
        self.deliberate()
        self.execute_plan()

        # ✅ Controle automático do modo de batalha
        if self.beliefs.get('target') is None or not getattr(self.beliefs['target'], 'beliefs', {}).get('is_alive', True):
            self.beliefs['em_batalha'] = False

        # print(f'INBOX DEPOIS: {self.inbox}')
        print(f'INTENÇÃO [{self.unique_id}]: {self.intention}')
        print(f'PLANO [{self.unique_id}]: {self.desires[0]}')
        # print(f'[{self.beliefs["name"]}] HP: {self.beliefs["hp"]}')
        print(f'Itens de cura: {self.beliefs["num_healing"]}')
        print(f'Em batalha: {self.beliefs["em_batalha"]}')
        print("-" * 40)

