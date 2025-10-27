from RPGModel import RPGModel
from mesa.visualization import (
    SolaraViz, 
    SpaceRenderer, 
    make_plot_component, 
    make_space_component
    )
from mesa.visualization.components import (
    AgentPortrayalStyle, PropertyLayerStyle
    )

def agent_portrayal(agent):
    return AgentPortrayalStyle(color="tab:orange", size=50)

def post_process(ax):
    """Customize the matplotlib axes after rendering."""
    ax.set_title("RPG Model")
    ax.set_xlabel("Largura")
    ax.set_ylabel("Altura")
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.5)
    ax.set_aspect("equal", adjustable="box")

def propertylayer_portrayal(layer):
    if layer.name == "test layer":
        return PropertyLayerStyle(color="blue", alpha=0.8, colorbar=True)

def agent_portrayal(agent):
    portrayal = AgentPortrayalStyle(size=50, color="black")
    return portrayal

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
    modelo_rpg = RPGModel(width=10, height=10, n=1)
    
    renderer = SpaceRenderer(model=modelo_rpg, backend="matplotlib").render(
        agent_portrayal=agent_portrayal
    )

    renderer.post_process = post_process
    # renderer.draw_propertylayer(propertylayer_portrayal)
    renderer.draw_agents(agent_portrayal)

    page = SolaraViz(
        modelo_rpg,
        renderer,
        components=[],
        model_params=model_params,
        name="RPG Model",
    )
    # This is required to render the visualization in the Jupyter notebook
    page
    