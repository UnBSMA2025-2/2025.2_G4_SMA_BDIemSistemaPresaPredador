from RPGModel import RPGModel
from mesa.visualization import SolaraViz, SpaceRenderer, make_plot_component
from mesa.visualization.components import AgentPortrayalStyle

def agent_portrayal(agent):
    return AgentPortrayalStyle(color="tab:orange", size=50)

model_params = {
    "n": {
        "type": "SliderInt",
        "value": 50,
        "label": "Number of agents:",
        "min": 10,
        "max": 100,
        "step": 1,
    },
    "width": 10,
    "height": 10,
}

if __name__ == "__main__":
    modelo_rpg = RPGModel()
    
    renderer = SpaceRenderer(model=modelo_rpg, backend="matplotlib").render(
        agent_portrayal=agent_portrayal
    )

    page = SolaraViz(
        modelo_rpg,
        renderer,
        components=[],
        model_params=model_params,
        name="RPG Model",
    )
    # This is required to render the visualization in the Jupyter notebook
    page
    