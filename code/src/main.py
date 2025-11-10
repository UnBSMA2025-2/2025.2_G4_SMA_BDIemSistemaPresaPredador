from components.agents_info import AgentInfo
from RPGModel import RPGModel
from mesa.visualization import (
    SolaraViz, 
    SpaceRenderer 
    )
from mesa.visualization.components import (
    AgentPortrayalStyle, PropertyLayerStyle
    )


def post_process(ax):
    """Personalize os eixos do matplotlib após a renderização."""
    ax.set_title("RPG Model")
    ax.set_xlabel("Largura")
    ax.set_ylabel("Altura")
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.5)
    ax.set_aspect("equal", adjustable="box")

def propertylayer_portrayal(layer):
    """
    Define como desenhar a camada de propriedade.
    Usamos 'colormap' para dados que variam (0s e 1s) -> Variar a coloração de acordo com o valor.
    """
    return PropertyLayerStyle(
        colormap="Greens",  # Um colormap que vai de "nada" (0) para "verde" (1)
        alpha=0.5,          # Transparência
        colorbar=False,     # Não mostrar a barra de legenda
        vmin=0,             # Mapear o valor 0 para a cor mais clara
        vmax=1              # Mapear o valor 1 para a cor mais escura (verde)
    )



def agent_portrayal(agent):
    portrayal = None
    if agent.type == 'CHARACTER':
        portrayal = AgentPortrayalStyle(size=50, color="black", marker="^")
    elif agent.type == 'ANIMAL':
        portrayal = AgentPortrayalStyle(size=50, color="gray")
    else:
        portrayal = AgentPortrayalStyle(size=50, color="red", marker="X")
    return portrayal

model_params = {
    "n": {
        "type": "SliderInt",
        "value": 3,
        "label": "Number of agents:",
        "min": 3,
        "max": 100,
        "step": 1,
    },
    "width": 40,  
    "height": 20,
}

if __name__ == "__main__":
    modelo_rpg = RPGModel(width=40, height=20, n=4)
    
    renderer = SpaceRenderer(model=modelo_rpg, backend="matplotlib").render(
        agent_portrayal=agent_portrayal,
        propertylayer_portrayal=propertylayer_portrayal,
        post_process=post_process
    )

    renderer.post_process = post_process
    renderer.draw_agents(agent_portrayal)

    page = SolaraViz(
        modelo_rpg,
        renderer,
        components=[AgentInfo],  # Adicionar componente de informações
        model_params=model_params,
        name="RPG Model",
    )

    page

