from communication import MessageDict
from Interfaces.IBDI_Agent import IBDI_Agent
from BDIPlanLogic.RetaliateAttackPlanLogic import RetaliateAttackPlanLogic
from BDIPlanLogic.EnemyDesires import get_desire
from utils.move_to_agent import move_to_agent
import uuid
import copy

class Mob_Agent(IBDI_Agent):
    """
    Um agente que representa um inimigo comum com lógica BDI.
    """
    def __init__(self, 
        model, 
        cell, 
        beliefs,
        type='ANIMAL'):
        super().__init__(model)
        self.cell = cell
        self.type = type
        self.visited_cells = {}
        self.plan_library = {
            'REACT': RetaliateAttackPlanLogic()
            }        
        self.inbox = []
        self.beliefs = copy.deepcopy(beliefs)
        self.desires = ['']
        self.intention = None

    def receive_attack(self, message):
        damage = message['content']['atk']- self.beliefs['def']
        newHp = self.beliefs['hp'] - max(0, damage)
        
        if newHp <= 0:
            self.beliefs['is_alive'] = False
            self.beliefs['hp'] = 0
        else:
            self.beliefs['hp'] = newHp
            self.beliefs['received_attack'] = message['sender']

        response = MessageDict(
            performative='ATTACK_RESPONSE',
            sender=self.unique_id,
            receiver=message['sender'],
            content={'is_alive': self.beliefs['is_alive']},
            conversation_id=message['conversation_id'])
        receiver = self.model.get_agent_by_id(
            message['sender'])
        receiver.inbox.append(response)

        if not self.beliefs['is_alive']:
            print(self.beliefs['is_alive'])
            self.remove()
        
        return
    
    def move_to_target(self, target_coordinate, displacement):
        h = self.model.grid.height
        l = self.model.grid.width
        
        if self.cell is  None:
            return False
        
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

        message = MessageDict(
            performative='ATTACK_TARGET',
            sender=self.unique_id,
            receiver=enemyAgent.unique_id,
            content={'atk': self.beliefs['atk']},
            conversation_id=uuid.uuid4()
        )

        enemyAgent.inbox.append(message)
        return

    def set_attacked_target(self):
        if self.beliefs['received_attack'] is not None:
            enemy = self.model.agents.select(
                lambda agent: agent.unique_id == self.beliefs['received_attack'])
            self.beliefs['target'] = next(iter(enemy))

            print(self.beliefs['target'])

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

    def update_desires(self):
        self.desires[0] = get_desire(self)
        pass

    def deliberate(self):
        self.intention = self.plan_library[self.desires[0]].get_intention(self)
        pass

    def execute_plan(self):
            match self.intention:
                case 'DEFINIR ALVO': # Resposta ao ataque do inimigo
                    self.set_attacked_target()
                    return
                
                case 'MOVER-SE': # Resposta ao ataque do inimigo
                    self.explore()
                    return
                
                case 'ATACAR': # Resposta ao ataque do inimigo
                    self.attack_enemy()
                    return
                
                case 'APROXIMAR-SE': # Resposta ao ataque do inimigo
                    if self.beliefs['target'] is not None:
                        if self.beliefs['target'].cell is not None:
                            self.move_to_target(
                                self.beliefs['target'].cell.coordinate,
                                self.beliefs['displacement'])
                            return
                        
                    self.explore()
                    return
                
                case _:
                    pass

    def process_message(self):
        for message in self.inbox:
            match message['performative']:
                case 'ATTACK_TARGET': # Resposta ao ataque do inimigo
                    self.receive_attack(message)
                
                case _:
                    pass
            self.inbox.remove(message)

    def process_message(self):
        for message in self.inbox:
            match message['performative']:
                case 'ATTACK_TARGET': # Resposta ao ataque do inimigo
                    self.receive_attack(message)
                
                case _:
                    pass
            self.inbox.remove(message)

    def step(self):

        print("-"*40)
        print(f"Executando step do animal...")
        print(f'INBOX: {self.inbox}')
        self.process_message()
        self.update_desires()
        self.deliberate()
        self.execute_plan()
        print(f'INTENÇÃO [{self.unique_id}]: {self.intention}')        
        print(f'CÉLULA [{self.unique_id}]: {self.cell}')        
        print("-"*40)