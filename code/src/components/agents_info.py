import solara
import os
import threading

AVATAR_PLACEHOLDER = "/assets/coelho.jpg"
BASE_DIR = os.path.dirname(__file__)
AVATAR_MAP = {
    "CHARACTER": os.path.join(BASE_DIR, "../assets/character.jpg"),
    "ANIMAL": os.path.join(BASE_DIR, "../assets/Slime_Rimuru.png"),
    "ENEMY": os.path.join(BASE_DIR, "../assets/goblin.jpg"),
}

STYLE_CARD_SCROLL = {
    "background-color": "rgb(25, 25, 25)",
    "color": "rgb(230, 230, 230)",
    "border": "4px solid rgb(80, 80, 80)",
    "border-radius": "8px",
    "font-family": "'Arial', 'Helvetica', sans-serif",
    "box-shadow": "0 6px 12px rgba(0,0,0,0.5)",
    "min-width": "700px",
    "resize": "both",
    "overflow": "auto",
}

STYLE_CELL_AVATAR = {"flex": "0 0 60px", "padding": "0 4px", "display": "flex", "align-items": "center", "justify-content": "center"}
STYLE_CELL_NORMAL = {"flex": "1", "padding": "0 6px"}
STYLE_HEADER_SCROLL = {"border-bottom": "2px solid rgb(80, 80, 80)", "padding": "10px 4px", "font-weight": "bold", "color": "rgb(255, 255, 255)"}
STYLE_DATA_SCROLL = {"border-bottom": "1px dashed rgb(60, 60, 60)", "padding": "8px 4px", "align-items": "center"}


@solara.component
def AgentInfo(model):
    refresh, set_refresh = solara.use_state(0)

    # Usar threading.Timer com cuidado para não criar múltiplos timers
    def periodic_refresh():
        set_refresh(lambda x: x + 1)
        # Inicia novo timer apenas se o componente ainda estiver ativo
        threading.Timer(1.0, periodic_refresh).start()

    # Inicia o timer apenas uma vez
    solara.use_effect(lambda: periodic_refresh(), [])

    agents_data = []
    for cell in model.grid.all_cells:
        if not cell.is_empty:
            for agent in cell.agents:
                avatar_url = AVATAR_MAP.get(agent.type, AVATAR_PLACEHOLDER)
                beliefs = getattr(agent, "beliefs", {})
                agent_info = {
                    "Avatar": avatar_url,
                    "Nome": beliefs.get("name", "-"),
                    "Tipo": agent.type,
                    "Intenção": getattr(agent, "intention", "Desconhecida"),
                    "Vida": beliefs.get("hp", "-"),
                    "Vida Máxima": beliefs.get("hpMax", "-"),
                    "Posição": f"({cell.coordinate[0]}, {cell.coordinate[1]})",
                    "Em Batalha": "Sim" if beliefs.get("in_battle") else "Não",
                    "Curas": beliefs.get("num_healing", "-"),
                }
                agents_data.append(agent_info)

    with solara.Card(elevation=8, style=STYLE_CARD_SCROLL):
        with solara.Div(style={"text-align": "center", "padding": "12px"}):
            solara.Markdown("## Quadro de Agentes", style={"color": "white"})

        if not agents_data:
            solara.Warning("Nenhum membro encontrado no quadro.")
            return

        keys = ["Avatar", "Nome", "Tipo", "Intenção", "Vida", "Posição", "Em Batalha", "Curas"]
        with solara.Row(style=STYLE_HEADER_SCROLL):
            for key in keys:
                style = STYLE_CELL_AVATAR if key == "Avatar" else STYLE_CELL_NORMAL
                solara.Markdown(f"**{key}**", style={"text-align": "center" if key == "Avatar" else "left", **style})

        for agent_data in agents_data[:10]:
            with solara.Row(style=STYLE_DATA_SCROLL):
                for key in keys:
                    value = agent_data.get(key, "-")
                    if key == "Avatar":
                        with solara.Div(style=STYLE_CELL_AVATAR):
                            solara.Image(str(value))

                    elif key == "Vida" and isinstance(value, (int, float)):
                        hpMax = agent_data.get('Vida Máxima', '-')
                        with solara.Div(style=STYLE_CELL_NORMAL):
                            color = "green" if value >= hpMax*0.3 else "red"
                            solara.ProgressLinear(value=(value / hpMax) * 100, color=color, style={"height": "12px", "border-radius": "6px"})
                            solara.Text(f"{int(value)}/{int(hpMax)} HP", style={"font-size": "0.8em", "text-align": "center"})

                    elif key == "Em Batalha":
                        with solara.Div(style=STYLE_CELL_NORMAL):
                            if value == "Sim":
                                # print("EStou em batalha")
                                solara.Text("⚔️ Em Combate", style={"font-size": "1em", "color": "red", "font-weight": "bold"})
                            else:
                                # print("Não estou em batalha")
                                solara.Text("🛡️ Seguro", style={"font-size": "1em", "color": "green"})
                                
                    else:
                        with solara.Div(style=STYLE_CELL_NORMAL):
                            solara.Text(str(value))

        if len(agents_data) > 10:
            solara.Info(f"Mostrando 10 de {len(agents_data)} membros da guilda.")
 