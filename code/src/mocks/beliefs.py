# caso onde o agente com pouca vida procura o alvo fraco para atacar
beliefs1 = {
    'name': 'Marllon',
    'hp': 1,
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
    'healing_item_spot': None,
    'target': None,
}

# caso onde o agente fica vários steps se curando
beliefs2 = {
    'name': 'Malbecky',
    'hp': 2000,
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
    'healing_item_spot': None,
    'target': None,
    'color': 'blue',
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
    'healing_item_spot': None,
    'target': None,
}


beliefs4 = {
    'name': 'Guerreiro',
    'hp': 65,
    'hpMax': 65,
    'is_alive': True,
    'def': 10,
    'atk': 25,
    'classe': 'GUERREIRO',
    'range': 0,
    'iniciativa': 11,
    'displacement': 1,
    'vision': 4,
    'em_batalha': False,
    'num_healing': 0,
    'healing_item_spot': None,
    'target': None,
    'color': 'black'
}

enemy_beliefs1 = {
    'name': 'Goblin',
    'hp': 65,
    'hpMax': 65,
    'is_alive': True,
    'def': 10,
    'atk': 15,
    'range': 2,
    'iniciativa': 14,
    'displacement': 2,
    'em_batalha': False,
    'target': None,
    'received_attack': None
}

animal_beliefs = {
    'name': 'Coelho',
    'hp': 10,
    'hpMax': 10,
    'is_alive': True,
    'def': 4,
    'iniciativa': 4,
    'displacement': 2,
}