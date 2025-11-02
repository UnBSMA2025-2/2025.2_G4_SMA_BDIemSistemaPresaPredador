def cond_low_life(agent):
    return agent.beliefs['hp'] < agent.beliefs['hpMax']*(0.3)

def cond_change_hp(agent):
    return agent.beliefs['hp'] != agent.beliefs['hpMax'] or agent.beliefs['received_attack'] is not None

def get_desire(agent):
    if cond_change_hp(agent=agent):
        return 'REACT'
    return 'REACT'