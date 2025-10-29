# caso onde o agente com pouca vida procura o alvo fraco para atacar
beliefs1 = {
    'name': 'Marllon',
    'hp': 10,
    'hpMax': 100,
    'is_alive': True,
    'def': 30,
    'att': 60,
    'classe': 'LADINO',
    'iniciativa': 14,
    'displacement':3,
    'em_batalha': True,
    'hp_agente_alvo': 40,
    'num_healing': 2,
    'target': None,
}

# caso onde o agente fica vários steps se curando
beliefs2 = {
    'name': 'Lucas',
    'hp': 1,
    'hpMax': 2000,
    'is_alive': True,
    'def': 10,
    'att': 100,
    'classe': 'MAGO',
    'iniciativa': 14,
    'displacement': 1,
    'em_batalha': False,
    'hp_agente_alvo': 9,
    'num_healing': 20,
    'target': None,
}

# caso onde o agente com pouca vida está fora de combate e em espera
beliefs3 = {
    'name': 'Lucas',
    'hp': 1,
    'hpMax': 2000,
    'is_alive': True,
    'def': 10,
    'att': 100,
    'classe': 'MAGO',
    'iniciativa': 14,
    'displacement': 1,
    'em_batalha': False,
    'hp_agente_alvo': 9,
    'num_healing': 0,
    'target': None,
}