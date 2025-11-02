def cond_low_life(agent):
    return agent.beliefs['hp'] < agent.beliefs['hpMax']*(0.3)

def cond_there_are_enemies(agent):
    enemies = agent.model.agents.select(
        lambda agent: agent.type != 'CHARACTER')
    return len(enemies) != 0 and agent.beliefs['hp'] >= agent.beliefs['hpMax']*(0.3)

def get_desire(agent):
    if cond_low_life(agent=agent):
        return 'SURVIVE'
    elif cond_there_are_enemies(agent=agent):
        return 'BATTLE'
    return None