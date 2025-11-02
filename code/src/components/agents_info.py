import solara
import os

# --- 1. Dicionários de Estilo (Tema "Escuro/Preto") ---

STYLE_CARD_SCROLL = {
    "background-color": "rgb(25, 25, 25)",  # Fundo preto/cinza escuro
    "color": "rgb(230, 230, 230)",        # Texto principal claro
    "border": "4px solid rgb(80, 80, 80)", # Borda cinza
    "border-radius": "8px",
    "font-family": "'Arial', 'Helvetica', sans-serif", # Fonte padrão
    "box-shadow": "0 6px 12px rgba(0,0,0,0.5)",
    "min-width": "700px", 
    "resize": "both",     
    "overflow": "auto",   
}

STYLE_CELL_AVATAR = {
    "flex": "0 0 60px", 
    "padding": "0 4px",
    "display": "flex",
    "align-items": "center",
    "justify-content": "center",
}

STYLE_CELL_NORMAL = {
    "flex": "1", 
    "padding": "0 6px",
    # Mantém a quebra de linha (sem corte de texto)
}

STYLE_HEADER_SCROLL = {
    "border-bottom": "2px solid rgb(80, 80, 80)", # Linha do cabeçalho cinza
    "padding": "10px 4px",
    "font-weight": "bold",
    "color": "rgb(255, 255, 255)", # Cabeçalho branco
}

STYLE_DATA_SCROLL = {
    "border-bottom": "1px dashed rgb(60, 60, 60)", # Linha de dados cinza
    "padding": "8px 4px",
    "align-items": "center",
}

# --- Mapeamento de Avatares ---
AVATAR_PLACEHOLDER = "/assets/coelho.jpg" 
BASE_DIR = os.path.dirname(__file__)
AVATAR_MAP = {
    "CHARACTER": os.path.join(BASE_DIR, "../assets/character.jpg"),
    "ANIMAL": os.path.join(BASE_DIR, "../assets/lobo.jpg"),
}

# --- 2. O Componente Atualizado ---

@solara.component
def AgentInfo(model):
    """Exibe informações dos agentes numa tabela estilizada (tema escuro)."""
    agents_data = []

    # --- Coleta de Dados (Sem alterações) ---
    for cell in model.grid.all_cells:
        if not cell.is_empty:
            for agent in cell.agents:
                agent_type = agent.type 
                avatar_url = AVATAR_MAP.get(agent_type, AVATAR_PLACEHOLDER)
                
                agent_info = {
                    "ID": agent.unique_id, "Tipo": agent.type,
                    "Posição": f"({cell.coordinate[0]}, {cell.coordinate[1]})",
                    "Avatar": avatar_url 
                }
                if hasattr(agent, 'beliefs'):
                    if 'name' in agent.beliefs: agent_info["Nome"] = agent.beliefs['name']
                    if 'hp' in agent.beliefs: agent_info["Vida"] = agent.beliefs['hp']
                    if 'em_batalha' in agent.beliefs: agent_info["Em Batalha"] = "Sim" if agent.beliefs['em_batalha'] else "Não"
                    if 'num_healing' in agent.beliefs: agent_info["Curas"] = agent.beliefs['num_healing']
                agents_data.append(agent_info)
    # --- Fim da Coleta de Dados ---

    # --- 3. Renderização do Componente ---

    with solara.Card(elevation=8, style=STYLE_CARD_SCROLL):
        with solara.Div(style={"text-align": "center", "padding": "12px"}):
            # --- Título com cor e fonte atualizadas ---
            solara.Markdown("## Quadro de Agentes",
                style={"color": "rgb(255, 255, 255)", "font-family": "'Arial', 'Helvetica', sans-serif"}
            )

        if agents_data:
            all_keys = set()
            for d in agents_data: all_keys.update(d.keys())
            preferred_order = ["Avatar", "ID", "Nome", "Tipo", "Vida", "Posição", "Em Batalha", "Curas"]
            keys = [key for key in preferred_order if key in all_keys] + \
                   [key for key in all_keys if key not in preferred_order]

            # --- 1. Linha do Cabeçalho ---
            with solara.Row(style=STYLE_HEADER_SCROLL):
                for key in keys:
                    style = STYLE_CELL_AVATAR if key == "Avatar" else STYLE_CELL_NORMAL
                    with solara.Div(style=style):
                        align = "center" if key == "Avatar" else "left"
                        solara.Markdown(f"**{key}**", style={"text-align": align})

            # --- 2. Linhas de Dados ---
            for agent_data in agents_data[:10]:
                with solara.Row(style=STYLE_DATA_SCROLL):
                    for key in keys:
                        value = agent_data.get(key, "-")
                        
                        if key == "Avatar":
                            with solara.Div(style=STYLE_CELL_AVATAR):
                                # "Porta-retrato" com borda cinza
                                with solara.Div(style={
                                    "width": "40px", "height": "40px", 
                                    "border-radius": "50%",
                                    "border": "2px solid rgb(80, 80, 80)", # --- COR ATUALIZADA ---
                                    "overflow": "hidden", "line-height": "0",
                                }):
                                    solara.Image(str(value))

                        elif key == "Vida" and isinstance(value, (int, float)):
                            with solara.Div(style=STYLE_CELL_NORMAL):
                                color = "green" if value >= 50 else "red"
                                solara.ProgressLinear(value=value, color=color, 
                                    style={"height": "12px", "border-radius": "6px"}
                                )
                                # Texto do HP já fica claro por padrão do STYLE_CARD_SCROLL
                                solara.Text(f"{int(value)}/100 HP", style={"font-size": "0.8em", "text-align": "center"})
                        
                        elif key == "Em Batalha":
                            with solara.Div(style=STYLE_CELL_NORMAL):
                                if value == "Sim":
                                    solara.Text("⚔️ Em Combate", style={"font-size": "1em", "color": "red", "font-weight": "bold"})
                                else:
                                    solara.Text("🛡️ Seguro", style={"font-size": "1em", "color": "green"})
                        
                        else:
                            with solara.Div(style=STYLE_CELL_NORMAL):
                                solara.Text(str(value))

            if len(agents_data) > 10:
                solara.Info(f"Mostrando 10 de {len(agents_data)} membros da guilda.")
        else:
            # O Solara Warning já se adapta bem ao tema escuro
            solara.Warning("Nenhum membro encontrado no quadro.")