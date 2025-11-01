import mesa
from mesa.discrete_space import OrthogonalMooreGrid
from Agents.character_agent import Character_Agent 
from Agents.enemy_agent import Enemy_Agent 
from mocks.beliefs import (
    beliefs1, 
    beliefs2, 
    beliefs3,
    beliefs4)

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
        
        Enemy_Agent.create_agents(
            model=self,
            cell=self.grid.all_cells.cells[1],
            n=self.num_agents,
            beliefs=beliefs1
        )
        # Character_Agent.create_agents(
        #     model=self,
        #     cell=self.grid.all_cells.cells[8],
        #     n=self.num_agents,
        #     beliefs=beliefs3
        # )
        Character_Agent.create_agents(
            model=self,
            cell=self.grid.all_cells.cells[2],
            n=self.num_agents,
            beliefs=beliefs2
        )

        agent1 = next(iter(self.agents.select(
            lambda agent: agent.unique_id == 1
        )))
        agent2 = next(iter(self.agents.select(
            lambda agent: agent.unique_id == 2
        )))

        agent1.beliefs['target'] = agent2
        agent2.beliefs['target'] = agent1

    def get_agent_by_id(self, agent_id):
        return (next(iter(self.agents.select(
            lambda agent: agent.unique_id == agent_id))))

    def step(self):
        print("\n" + "="*40)
        print(f"--- Início do Passo {self.steps} da Simulação ---")

        self.message_box = {}
        
        self.agents.shuffle_do("step")
        
        print("="*40)