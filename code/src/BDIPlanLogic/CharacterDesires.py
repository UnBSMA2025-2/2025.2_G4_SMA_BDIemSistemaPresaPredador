def cond_low_life(agent):
    return agent.beliefs['hp'] < agent.beliefs['hpMax']*(0.3)

def cond_there_are_enemies(agent):
    enemies = agent.model.agents.select(
        lambda agent: agent.type != 'CHARACTER')
    return len(enemies) != 0 and agent.beliefs['hp'] >= agent.beliefs['hpMax']*(0.3)

def cond_there_are_enemies_nearby(agent):
    """
    Verifica se existe um inimigo DENTRO DO ALCANCE de percepção do agente.
    """
    range_de_visao = agent.beliefs.get('displacement', 1) # Usar 1 como default se não existir
    
    vizinhos = agent.cell.get_neighborhood(range_de_visao).cells 
    
    for cell in vizinhos:
        if len(cell.agents) > 0 and cell.agents[0] is not None:
            if hasattr(cell.agents[0], 'type') and cell.agents[0].type != 'CHARACTER':
                # Encontrou um inimigo
                return True
    
    # Não encontrou inimigos por perto
    return False

def get_desire(agent):
    if cond_low_life(agent=agent):
        return 'SURVIVE'
    elif cond_there_are_enemies_nearby(agent=agent):
        return 'BATTLE'
    return 'EXPLORE'