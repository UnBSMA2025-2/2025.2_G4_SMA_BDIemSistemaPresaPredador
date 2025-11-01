# caso onde o agente com pouca vida procura o alvo fraco para atacar
beliefs1 = {
    'name': 'Marllon',
    'hp': 10,
    'hpMax': 100,
    'is_alive': True,
    'def': 30,
    'atk': 60,
    'classe': 'LADINO',
    'range': 1,
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
    'atk': 100,
    'classe': 'MAGO',
    'range': 5,
    'iniciativa': 14,
    'displacement': 10,
    'em_batalha': False,
    'hp_agente_alvo': 9,
    'num_healing': 20,
    'target': None,
}

# caso onde o agente com pouca vida está fora de combate e espera ou tem um amigo ao lado
beliefs3 = {
    'name': 'Toni',
    'hp': 1,
    'hpMax': 2000,
    'is_alive': True,
    'def': 10,
    'atk': 100,
    'classe': 'MAGO',
    'range': 5,
    'iniciativa': 14,
    'displacement': 10,
    'em_batalha': False,
    'hp_agente_alvo': 9,
    'num_healing': 0,
    'target': None,
}


beliefs4 = {
    'name': 'Lucas',
    'hp': 1,
    'hpMax': 2000,
    'is_alive': True,
    'def': 10,
    'atk': 100,
    'classe': 'GUERREIRO',
    'range': 5,
    'iniciativa': 14,
    'displacement': 1,
    'em_batalha': True,
    'hp_agente_alvo': 9,
    'num_healing': 20,
    'target': None,
}