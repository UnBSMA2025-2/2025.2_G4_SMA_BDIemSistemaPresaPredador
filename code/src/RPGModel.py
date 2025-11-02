import mesa
from mesa.discrete_space import OrthogonalMooreGrid
from Agents.character_agent import Character_Agent 
from Agents.mob_agent import Mob_Agent 
from mocks.beliefs import (
    beliefs1, 
    beliefs2, 
    beliefs3,
    beliefs4,
    enemy_beliefs1)

class RPGModel(mesa.Model):
    """
    Modelo MESA para simular o mundo do RPG.
    """
    
    def __init__(self, width=10, height=10, seed=None, n=5, some_kwarg_I_need=True):
        """
        Inicializa o modelo, o scheduler e cria o agente único.
        """
        super().__init__(seed=seed)
        self.message_box = {}
        self.num_agents = n
        self.grid = OrthogonalMooreGrid(
            (width, height), torus=True, capacity=1, random=self.random
        )
        
        Mob_Agent.create_agents(
            model=self,
            cell=self.random.choices(self.grid.all_cells.cells, k=self.num_agents),
            n=self.num_agents,
            beliefs=enemy_beliefs1
        )
        # Character_Agent.create_agents(
        #     model=self,
        #     cell=self.random.choices(self.grid.all_cells.cells, k=self.num_agents),
        #     n=self.num_agents,
        #     beliefs=beliefs1,
        #     type='ENEMY'
        # )
        Character_Agent.create_agents(
            model=self,
            cell=self.random.choices(self.grid.all_cells.cells, k=self.num_agents),
            n=self.num_agents,
            beliefs=beliefs4
        )

    def get_agent_by_id(self, agent_id):
        return (next(iter(self.agents.select(
            lambda agent: agent.unique_id == agent_id))))

    def step(self):
        print("\n" + "="*40)
        print(f"--- Início do Passo {self.steps} da Simulação ---")

        self.message_box = {}
        
        self.agents.shuffle_do("step")
        
        print("="*40)