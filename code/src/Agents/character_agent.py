from Interfaces.IBDI_Agent import IBDI_Agent
from utils.move_to_agent import move_to_agent
from Beliefs.SurvivePlanLogic import SurvivePlanLogic
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
        beliefs
        ):
        super().__init__(model)
        self.cell = cell
        self.type = 'CHARACTER'
        self.plan_library = {
        'SURVIVE': SurvivePlanLogic()
        }        
        self.received_messages = []
        self.beliefs = beliefs
        self.desires = ['SURVIVE']
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
            self.cell = new_cell

    def attack_enemy(self):
        enemyAgent = self.beliefs['target']

        damage = self.beliefs['att'] - enemyAgent.beliefs['def']
        newHpEnemy = enemyAgent.beliefs['hp'] - max(0, damage)
        
        if newHpEnemy <= 0:
            enemyAgent.beliefs['is_alive'] = False
            enemyAgent.beliefs['hp'] = 0
        else:
            enemyAgent.beliefs['hp'] = newHpEnemy

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
                self.model.send_message(message)
                print(f'PEDIDO DE CURA ENVIADO')
                return

    def escape(self):
        vizinho = self.cell.neighborhood.select_random_cell()
        
        self.move_to_target(vizinho.coordinate, 1)

    def get_heal(self, message):
        '''
        Método para receber uma cura via mensagem
        '''
        self.beliefs['num_healing'] += message['content']['num_healing']
        print(f'CURA RECEBIDA')
        return

    def send_heal(self, message):
        """
        Método para enviar uma cura por mensagem
        """
        response = MessageDict(
            performative='GET_HEALING',
            sender=self.unique_id,
            receiver=message['sender'],
            content={'num_healing': 1},
            conversation_id=message['conversation_id']
        )
        self.model.send_message(response)
        self.beliefs['num_healing'] -= 1
        print(f'CURA ENVIADA')
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
                pass

            case _:
                pass

    def process_message(self):
        for message in self.received_messages:
            match message['performative']:
                case 'SEND_HEALING': # Envia uma acura
                    self.send_heal(message)
                    pass
                case 'GET_HEALING': # Recebe a acura
                    self.get_heal(message)
                    pass
                case 'ATTACK_TARGET': # Envia um ataque
                    pass
                case _:
                    pass
            self.received_messages.remove(message)

    def get_messages(self):
        self.received_messages = self.model.get_messages(self.unique_id)
        pass

    def step(self):
        print("-"*40)
        print(f"Executando step do personagem...")
        self.get_messages()
        self.process_message()
        self.update_desires()
        self.deliberate()
        self.execute_plan()
        print(f'INTENÇÃO [{self.unique_id}]: {self.intention}')        
        print("-"*40)
