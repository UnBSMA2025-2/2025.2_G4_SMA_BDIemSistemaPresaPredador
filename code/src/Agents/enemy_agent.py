import random
from Interfaces.IBDI_Agent import IBDI_Agent
from communication import MessageDict

class Enemy_Agent(IBDI_Agent):
    """
    Um agente que representa um inimigo comum com lógica BDI.
    """
    def __init__(self, 
        model, 
        cell, 
        beliefs,
        type='ANIMAL'):
        super().__init__(model)
        self.cell = cell
        self.type = type

        self.plan_library = {}        
        self.inbox = []
        self.beliefs = beliefs
        self.desires = []
        self.intention = None

    def receive_attack(self, message):
        damage = message['content']['atk']- self.beliefs['def']
        newHp = self.beliefs['hp'] - max(0, damage)
        
        if newHp <= 0:
            self.beliefs['is_alive'] = False
            self.beliefs['hp'] = 0
        else:
            self.beliefs['hp'] = newHp

        response = MessageDict(
            performative='ATTACK_RESPONSE',
            sender=self.unique_id,
            receiver=message['sender'],
            content={'is_alive': self.beliefs['is_alive']},
            conversation_id=message['conversation_id'])
        receiver = self.model.get_agent_by_id(
            message['sender'])
        receiver.inbox.append(response)

        print(f'MENSAGEM DE RESPOSTA: {message}')
        
        return
   
    def update_desires(self):
        pass

    def deliberate(self):
        self.intention = self.plan_library[self.desires[0]].get_intention(self)

    def execute_plan(self):
            pass

    def process_message(self):
        for message in self.inbox:
            match message['performative']:
                case 'ATTACK_TARGET': # Resposta ao ataque do inimigo
                    self.receive_attack(message)
                    return
                
                case _:
                    pass
            self.inbox.remove(message)

    def process_message(self):
        for message in self.inbox:
            match message['performative']:
                case 'ATTACK_TARGET': # Resposta ao ataque do inimigo
                    self.receive_attack(message)
                    return
                
                case _:
                    pass
            self.inbox.remove(message)

    def step(self):
        print("-"*40)
        print(f"Executando step do animal...")
        print(f'INBOX: {self.inbox}')
        self.process_message()
        self.update_desires()
        self.deliberate()
        self.execute_plan()
        print(f'INTENÇÃO [{self.unique_id}]: {self.intention}')        
        # print(f'CRENÇAS [{self.unique_id}]: {self.beliefs}')        
        print("-"*40)