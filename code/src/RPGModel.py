import mesa
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.discrete_space.property_layer import PropertyLayer
from Agents.character_agent import Character_Agent 
from Agents.mob_agent import Mob_Agent
from Agents.animal_agent import Animal_Agent 
from mocks.beliefs import (
    beliefs4,
    enemy_beliefs1,
    animal_beliefs)

class RPGModel(mesa.Model):
    """
    Modelo MESA para simular o mundo do RPG.
    """
    
    def __init__(self, width=10, height=10, seed=None, n=5, some_kwarg_I_need=True):
        """
        Inicializa o modelo, o scheduler e cria o agente único.
        """
        super().__init__(seed=seed)
        self.num_agents = n
        
        self.grid = OrthogonalMooreGrid(
            (width, height), torus=True, capacity=1, random=self.random
        )

        healing_item_prob = 0.035 # 5% de chance de ter item de cura em uma das células do grid

        layer_name = "healing_item_spot"

        healing_layer = PropertyLayer(
            layer_name, 
            dimensions=self.grid.dimensions, 
            dtype=int,
            default_value=0
        )

        for cell in self.grid.all_cells.cells:
            cell_value = 1 if self.random.random() <= healing_item_prob else 0

            x, y = cell.coordinate

            healing_layer.data[x, y] = cell_value


            if not hasattr(cell, 'beliefs'):
                cell.beliefs = {}
            cell.beliefs['healing_item_spot'] = (cell_value == 1)

            setattr(cell, layer_name, cell_value)

        self.grid.add_property_layer(healing_layer)

        # Referência para que os agentes possam acessar a camada de cura
        self.healing_layer = healing_layer

        Mob_Agent.create_agents(
            model=self,
            cell=self.random.choices(self.grid.all_cells.cells, k=self.num_agents),
            n=self.num_agents,
            beliefs=enemy_beliefs1
        )
        Character_Agent.create_agents(
            model=self,
            cell=self.random.choices(self.grid.all_cells.cells, k=self.num_agents),
            n=self.num_agents,
            beliefs=beliefs4
        )
        Animal_Agent.create_agents(
            model=self,
            cell=self.random.choices(self.grid.all_cells.cells, k=self.num_agents),
            n=self.num_agents,
            beliefs=animal_beliefs
        )

    def get_agent_by_id(self, agent_id):
        try:
            agent = (next(iter(self.agents.select(
                lambda agent: agent.unique_id == agent_id))))
            return agent
        except:
            return None


    def get_invalid_cells(self):
        character_agents = self.agents.select(
            lambda agent: agent.type == 'CHARACTER')
        
        celulas_invalidas = []

        for agent in character_agents:
            vizinhos = agent.cell.get_neighborhood(
                agent.beliefs['vision']).cells
            celulas_invalidas += vizinhos

        print(f'character_agents: {celulas_invalidas}')
        return set(celulas_invalidas)


    def step(self):
        print("\n" + "="*40)
        print(f"--- Início do Passo {self.steps} da Simulação ---")

        self.agents.shuffle_do("step")
        
        print("="*40)