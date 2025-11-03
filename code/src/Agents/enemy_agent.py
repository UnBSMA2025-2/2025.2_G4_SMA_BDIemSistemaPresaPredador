import random
import uuid
from Interfaces.IBDI_Agent import IBDI_Agent
from communication import MessageDict
from BDIPlanLogic.EnemyAgentPlanLogic import EnemyAgentPlanLogic
from utils.move_to_agent import move_to_agent

class Enemy_Agent(IBDI_Agent):
    """
    Um agente que representa um inimigo comum com lógica BDI.
    """
    def __init__(
        self, 
        model, 
        cell, 
        beliefs,
        type='ANIMAL'
        ):
        
        super().__init__(model)
        self.cell = cell
        self.type = type
        self.plan_library = {
            'SURVIVE': EnemyAgentPlanLogic()
        }

        self.inbox = []
        self.beliefs = beliefs
        self.desires = ['SURVIVE']
        self.intention = None

    def move_to_target(self, target_coordinate, displacement=1):
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
            return True
        else:
            return False
        
    def move_around(self):
        vizinho = self.cell.neighborhood.select_random_cell()
        
        self.move_to_target(vizinho.coordinate, 1)

    def flee_and_heal(self):
        for step in range(self.beliefs['displacement']):
            neighbor = self.cell.neighborhood.select_random_cell()
            while not self.move_to_target(neighbor.coordinate):
                neighbor = self.cell.neighborhood.select_random_cell()
                
        newHp = self.beliefs['hp'] + random.randint(2, 4)
        if newHp > self.beliefs['hpMax']:
            self.beliefs['hp'] = self.beliefs['hpMax']
        else:
            self.beliefs['hp'] = newHp
        
    def heal(self):
        newHp = self.beliefs['hp'] + random.randint(5, 10)
        if newHp > self.beliefs['hpMax']:
            self.beliefs['hp'] = self.beliefs['hpMax']
        else:
            self.beliefs['hp'] = newHp     
    
    def set_target(self, size=5):
        """
        Busca por um alvo em uma área quadrada de `size` x `size` centrada na célula atual.
        size deve ser ímpar (ex.: 5 -> raio 2).
        """
        center = self.cell.coordinate
        radius = size // 2

        min_x = max(0, center[0] - radius)
        max_x = min(self.model.grid.width - 1, center[0] + radius)
        min_y = max(0, center[1] - radius)
        max_y = min(self.model.grid.height - 1, center[1] + radius)

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if (x, y) == tuple(center):
                    continue

                cell = next(iter(self.model.grid.all_cells.select(
                    lambda c: c.coordinate == (x, y)
                )), None)
                if len(cell.agents) != 0:
                    if cell.agents[0].type == 'CHARACTER':
                        self.beliefs['target'] = cell.agents[0]
                        self.beliefs['em_batalha'] = True
                        return
    
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
            receiver=message['sender'],
            content={'is_alive': self.beliefs['is_alive']},
            conversation_id=message['conversation_id']
        )
        
        receiver = self.model.get_agent_by_id(message['sender'])
        
        if receiver is not None:
            receiver.inbox.append(response)        
        
        if not self.beliefs['is_alive']:
            self.remove()
        
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
            case 'FUGIR':
                self.flee_and_heal()
                return
            
            case 'ATACAR INIMIGO':
                self.attack_enemy()
                return
            
            case 'APROXIMAR-SE':
                print(f'POSIÇÃO: {self.cell.coordinate}')
                self.move_to_target(
                    self.beliefs['target'].cell.coordinate,
                    self.beliefs['displacement']
                )
                print(f'POSIÇÃO NOVA: {self.cell.coordinate}')
                return
            
            case 'CURAR':
                self.heal()
                return
            
            case 'EXPLORAR':
                self.move_around()
                self.set_target()
                return
            
            case _:
                pass

    def process_message(self):
        for message in self.inbox:
            match message['performative']:
                case 'ATTACK_TARGET':
                    self.receive_attack(message)
                
                case 'ATTACK_RESPONSE':
                    self.attack_response(message)
                
                case _:
                    pass
            self.inbox.remove(message)

    def step(self):
        print(f"Executando step do inimigo...")
        print(f'INBOX: {self.inbox}')
        self.process_message()
        self.update_desires()
        self.deliberate()
        self.execute_plan()
        print(f'INTENÇÃO [{self.unique_id}]: {self.intention}')           
        print("-"*40)