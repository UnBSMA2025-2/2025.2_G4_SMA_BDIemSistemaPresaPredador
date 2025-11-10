from communication import MessageDict
from Interfaces.IBDI_Agent import IBDI_Agent
from BDIPlanLogic.SurviveAnimalPlanLogic import SurviveAnimalPlanLogic 
from BDIPlanLogic.AnimalDesires import get_desire
from utils.move_to_agent import move_to_agent
import uuid
import copy

class Animal_Agent(IBDI_Agent):
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
            'SURVIVE': SurviveAnimalPlanLogic()
            }        
        self.inbox = []
        self.beliefs = copy.deepcopy(beliefs)
        self.desires = ['']
        self.intention = None


    # ---------------------- EXPLORAÇÃO ---------------------- #
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
    
    def escape(self):
        if self.cell is not None:
            vizinho = self.cell.neighborhood.select_random_cell()
            self.move_to_target(vizinho.coordinate, 1)
    
    # ---------------------- CICLO BDI ---------------------- #
    def update_desires(self):
        self.desires[0] = get_desire(self)
        pass

    def deliberate(self):
        self.intention = self.plan_library[self.desires[0]].get_intention(self)
        pass

    def execute_plan(self):
            match self.intention:
                case 'EXPLORAR':
                    print(f'INTENÇÃO DO ANIMAL: {self.intention}')
                    self.explore()
                    return
                
                case 'FUGIR':
                    self.escape()
                    return
                case _:
                    pass

    def process_message(self): pass

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