from Interfaces.IBDI_Agent import IBDI_Agent
from utils.move_to_agent import move_to_agent
from Beliefs.SurvivePlanLogic import SurvivePlanLogic
from Beliefs.BattlePlanLogic import BattlePlanLogic
from Beliefs.ExplorationPlanLogic import ExplorationPlanLogic
import random
from communication import MessageDict
import uuid

class Character_Agent(IBDI_Agent):
    """
    Um agente que representa um personagem de RPG com lógica BDI.
    """
    def __init__(
        self, 
        model, 
        cell, 
        beliefs,
        type='CHARACTER'
        ):
        super().__init__(model)
        self.cell = cell
        self.type = type
        self.plan_library = {
        'SURVIVE': SurvivePlanLogic(),
        'BATTLE': BattlePlanLogic(),
        'EXPLORE': ExplorationPlanLogic(),
        }        
        self.inbox = []
        self.beliefs = beliefs
        self.desires = ['BATTLE', 'SURVIVE', 'EXPLORE']
        self.intention = None

    def get_friends(self):
        vizinhos = self.cell.get_neighborhood(
            self.beliefs['displacement'])
        
        cell_agentes_amigos = vizinhos.select(
            lambda cell: not cell.is_empty and next(iter(cell.agents)).type == 'CHARACTER').cells
    
        return cell_agentes_amigos

    def move_to_target(self, target_coordinate, displacement):
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
        
        if new_cell.is_empty:
            try:
                self.model.grid.move_agent(self, new_position)
            except Exception:
                self.model.grid.place_agent(self, new_position)
            # atualiza referência local à célula
            self.cell = new_cell

    def attack_enemy(self):
        enemyAgent = self.beliefs['target']

        message = MessageDict(
            performative='ATTACK_TARGET',
            sender=self.unique_id,
            receiver=enemyAgent.unique_id,
            content={'atk': self.beliefs['atk']},
            conversation_id=uuid.uuid4()
        )
        enemyAgent.inbox.append(message)
        return

    def heal(self):
        if self.beliefs['num_healing'] > 0:
            self.beliefs['hp'] += random.randint(1, 4)
            self.beliefs['num_healing'] -= 1

    def request_heal(self):
        '''
        Método solicitar uma cura via mensagem
        '''
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
        vizinho = self.cell.neighborhood.select_random_cell()
        
        self.move_to_target(vizinho.coordinate, 1)

    def set_target(self):
        vizinhos = self.cell.neighborhood.cells
        for cell in vizinhos:
            if len(cell.agents) != 0:
                    if cell.agents[0].type != 'CHARACTER':
                        self.beliefs['target'] = cell.agents[0]
                        return

    def set_friens_target(self):
        vizinhos = self.cell.get_neighborhood(
                self.beliefs['displacement']).cells 
        for cell in vizinhos:
            if len(cell.agents) != 0:
                if cell.agents[0].type == 'CHARACTER' and cell.agents[0].beliefs['em_batalha']:
                    self.beliefs['target'] = cell.agents[0].beliefs['target']

    def set_other_target(self):
        mapa = self.model.grid.all_cells.cells
        for cell in mapa:
            if len(cell.agents) != 0:
                if cell.agents[0].type != 'CHARACTER':
                    self.beliefs['target'] = cell.agents[0]
                    self.beliefs['em_batalha'] = True
                    return

    def get_heal(self, message):
        '''
        Método para receber uma cura via mensagem
        '''
        self.beliefs['num_healing'] += message['content']['num_healing']
        return

    def send_heal(self, message):
        """
        Método para enviar uma cura por mensagem
        """
        receiver = self.model.get_agent_by_id(
            message['sender'])
        
        response = MessageDict(
            performative='GET_HEALING',
            sender=self.unique_id,
            receiver=receiver.unique_id,
            content={'num_healing': 1},
            conversation_id=message['conversation_id']
        )

        receiver.inbox.append(response)
        self.beliefs['num_healing'] -= 1
        return
        
    def receive_attack(self, message):
        damage = message['content']['atk']- self.beliefs['def']
        newHp = self.beliefs['hp'] - max(0, damage)
        
        if newHp <= 0:
            self.beliefs['is_alive'] = False
            self.beliefs['hp'] = 0
        else:
            self.beliefs['hp'] = newHp

        response = MessageDict(
            performative='ATTACK_RESPONSE',
            sender=self.unique_id,
            receiver=message.unique_id,
            content={'is_alive': self.beliefs['is_alive']},
            conversation_id=message['conversation_id'])
        receiver = self.model.get_agent_by_id(
            message['sender'])
        receiver.inbox.append(response)
        
        return
    
    def attack_response(self, message):
        if not message['content']['is_alive']:
            self.beliefs['target'] = None
            self.beliefs['em_batalha'] = False
        return

    # -------- BDI -------- #
    def update_desires(self):
        pass

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
                self.move_to_target(
                    self.beliefs['target'].cell.coordinate,
                    self.beliefs['displacement'])
                return

            case 'FUGIR':
                self.escape()
                return

            case 'APROXIMAR-SE DE AMIGO':
                for cell in self.get_friends():
                    if not cell.agents[0].beliefs['em_batalha']:
                        friend_pos = cell.agents[0].cell.coordinate
                        self.move_to_target(
                            friend_pos,
                            self.beliefs['displacement'])
                        return

            case 'OBTER CURA':
                self.request_heal()
                return

            case 'ESPERAR':
                return

            case 'DEFINIR ALVO':
                self.set_target()
                return

            case 'DEFINIR ALVO DO AMIGO':
                self.set_friens_target()
                return

            case 'DEFINIR OUTRO ALVO':
                self.set_other_target()
                return
            
            case 'EXPLORAR MAPA':
                vizinho = self.cell.neighborhood.select_random_cell()
                self.move_to_target(
                    vizinho.coordinate,
                    self.beliefs['displacement'])
                return

            case 'APROXIMAR DO ITEM':
                item_pos = self.beliefs['healing_item_spot']
                self.move_to_target(
                    item_pos,
                    self.beliefs['displacement'])
                return

            case 'ADQUIRIR ITEM':
                self.beliefs['num_healing'] += 1
                self.cell.beliefs['healing_item_spot'] = False
                self.beliefs['healing_item_spot'] = None
                return

            case _:
                pass

    def process_message(self):
        for message in self.inbox:
            match message['performative']:
                case 'SEND_HEALING': # Envia uma acura
                    self.send_heal(message)
                    return

                case 'GET_HEALING': # Recebe a acura
                    self.get_heal(message)
                    return

                case 'ATTACK_TARGET': # Envia um ataque
                    self.receive_attack(message)
                    return

                case 'ATTACK_RESPONSE': # Resposta ao ataque do inimigo
                    self.attack_response(message)
                    print(self.beliefs['em_batalha'])
                    return
                case _:
                    pass
            self.inbox.remove(message)

    def step(self):
        print("-"*40)
        print(f"Executando step do personagem...")
        print(f'INBOX: {self.inbox}')
        self.process_message()
        self.update_desires()
        self.deliberate()
        self.execute_plan()
        print(f'INTENÇÃO [{self.unique_id}]: {self.intention}')        
        # print(f'CRENÇAS [{self.unique_id}]: {self.beliefs}')        
        print("-"*40)
