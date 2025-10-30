import random
from Interfaces.IBDI_Agent import IBDI_Agent
from Beliefs.SurvivePlanLogic import SurvivePlanLogic
from utils.move_to_agent import move_to_agent

class Enemy_Agent(IBDI_Agent):
    """
    Um agente que representa um inimigo comum com lógica BDI.
    """
    def __init__(
        self,
        model,
        cell,
        beliefs
        ):
        super().__init__(model)
        self.cell = cell
        self.type = 'COMMON_ENEMY'
        self.plan_library = {
            'SURVIVE': SurvivePlanLogic()
        }

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

    def flee_and_heal(self):
        for step in range(self.beliefs['displacement']):
            neighbor = self.cell.neighborhood.select_random_cell()
            while not self.move_to_target(neighbor.coordinate):
                neighbor = self.cell.neighborhood.select_random_cell()
        self.beliefs['hp'] += random.randint(2, 4)
        
    def attack_enemy(self):
        enemyAgent = self.beliefs['target']
        
        damage = self.beliefs['att'] - enemyAgent.beliefs['def']
        newHpEnemy = enemyAgent.beliefs['hp'] - max(0, damage)
        
        if newHpEnemy <= 0:
            enemyAgent.beliefs['is_alive'] = False
            enemyAgent.beliefs['hp'] = 0
        else:
            enemyAgent.beliefs['hp'] = newHpEnemy
        print(f'ATAQUE REALIZADO [{self.unique_id} atacou {self.beliefs['target'].unique_id}]\n----> DANO CAUSADO: {damage}')

    # -------- BDI -------- #
    def update_beliefs(self):
        pass

    def deliberate(self):
        self.intention = self.plan_library[self.desires[0]].get_intention(self)

    def execute_plan(self):
        match self.intention:
            case 'CURAR':
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
            
            case 'FUGIR':
                self.flee_and_heal()
                return
            
            case _:
                pass

    def step(self):
        print(f"Executando step do inimigo...")
        self.update_beliefs()
        self.deliberate()
        self.execute_plan()
        print(f'INTENÇÃO [{self.unique_id}]: {self.intention}')        
        print(f'AGENTE [{self.unique_id}]: {self.beliefs}')