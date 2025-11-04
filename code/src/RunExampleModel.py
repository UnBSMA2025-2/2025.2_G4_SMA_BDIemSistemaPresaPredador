from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from exampleModel import MoneyModel

def agent_portrayal(agent):
    """Define como os agentes serão desenhados com base na sua riqueza."""
    portrayal = {"Shape": "circle", "Filled": "true", "Layer": 0}

    if agent.wealth == 0:
        portrayal["Color"] = "grey"
        portrayal["r"] = 0.2
    elif agent.wealth == 1:
        portrayal["Color"] = "yellow"
        portrayal["r"] = 0.4
    elif agent.wealth == 2:
        portrayal["Color"] = "orange"
        portrayal["r"] = 0.6
    elif agent.wealth == 3:
        portrayal["Color"] = "red"
        portrayal["r"] = 0.8
    else: # Riqueza maior que 3
        portrayal["Color"] = "green"
        portrayal["r"] = 1
        
    return portrayal

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

# CRIAÇÃO DO GRÁFICO
chart = ChartModule([{"Label": "Gini",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

# Cria o servidor
server = ModularServer(MoneyModel,
                       [grid, chart],
                       "Money Model",
                       {"N": 100, "width": 20, "height": 20})

server.port = 8521 # Porta padrão para o servidor
server.launch()