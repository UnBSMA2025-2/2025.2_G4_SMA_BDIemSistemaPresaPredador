
# def cond_other_agents_nearby(agent):
#     vizinhos = agent.cell.neighborhood
#     for cell in vizinhos:
#         if cell.agents[0].type != 'ANIMAL':
#             return True
#     return False

def get_desire(agent):
    # if cond_other_agents_nearby(agent=agent):
    #     return 'SURVIVE'
    return 'SURVIVE'