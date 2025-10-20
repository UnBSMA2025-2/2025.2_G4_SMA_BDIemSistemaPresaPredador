from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np

class MoneyAgent(Agent):
    """Um agente que tem uma quantidade de dinheiro."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1 # Cada agente começa com 1 de riqueza

    def step(self):
        # O agente não faz nada se não tiver dinheiro
        if self.wealth == 0:
            return

        # Escolhe outro agente aleatoriamente
        other_agent = self.random.choice(self.model.schedule.agents)

        # E dá uma unidade de dinheiro a ele
        if other_agent is not None:
            other_agent.wealth += 1
            self.wealth -= 1

def compute_gini(model):
    """Calcula o coeficiente de Gini para medir a desigualdade de riqueza."""
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return (1 + (1 / N) - 2 * B)

class MoneyModel(Model):
    """Um modelo com um número de agentes."""
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Cria os agentes
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        # Coletor de dados ATUALIZADO
        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini}, 
            agent_reporters={"Wealth": "wealth"}  
        )

    def step(self):
        """Executa um passo do modelo."""
        self.datacollector.collect(self)
        self.schedule.step()