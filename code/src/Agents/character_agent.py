from Interfaces.IBDI_Agent import IBDI_Agent
from utils.move_to_agent import move_to_agent
from utils.get_intention_id import get_intention_id
from Beliefs.SurvivePlanLogic import SurvivePlanLogic


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
        
        self.plan_library = {
        'SURVIVE': SurvivePlanLogic()
        }         
        
        self.beliefs = beliefs
        self.desires = ['SURVIVE']
        self.intention = None

    def move_to_target(self, target_coordinate=(0,0), h=10, l=10):
        pos_a = self.cell.coordinate
        pos_b = target_coordinate
        
        new_position = move_to_agent(
            h, 
            l, 
            pos_a[0],
            pos_a[1],
            pos_b[0], 
            pos_b[1], 
            self.beliefs['deslocamento']
        )
        
        new_cell = next(iter(self.model.grid.all_cells.select(
            lambda cell: cell.coordinate == new_position
        )))
        
        if new_cell.is_empty:
            self.cell = new_cell
        else:
            if target_coordinate[0] == 0: return self.move_to_target(
                (target_coordinate[0]+1, target_coordinate[1]), h, l
            )
            elif target_coordinate[0] == h: return self.move_to_target(
                (target_coordinate[0]-1, target_coordinate[1]), h, l
            )
            elif target_coordinate[1] == 0: return self.move_to_target(
                (target_coordinate[0], target_coordinate[1]+1), h, l
            )
            elif target_coordinate[1] == l: return self.move_to_target(
                (target_coordinate[0], target_coordinate[1]-1), h, l
            )
 
    def update_beliefs(self):
        pass

    def deliberate(self):
        self.intention = self.plan_library[self.desires[0]].get_intention(self.beliefs)

    def execute_plan(self):
        pass

    def step(self):
        print(f"Executando step do personagem...")
        self.update_beliefs()
        self.deliberate()
        self.execute_plan()
        print(self.intention)