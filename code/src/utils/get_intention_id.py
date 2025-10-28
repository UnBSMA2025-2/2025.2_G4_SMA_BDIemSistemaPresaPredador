def get_intention_id(vector):
    intention_id = 0
    for condition in vector:
        # Usa o operador 'OU' bit-a-bit para "ligar" o bit
        # (1 << indice) cria um número com apenas o bit 'indice' ligado
        # (ex: 1 << 2 é 100 em binário, que é 4)
        intention_id = intention_id | (1 << condition)
    return intention_id
