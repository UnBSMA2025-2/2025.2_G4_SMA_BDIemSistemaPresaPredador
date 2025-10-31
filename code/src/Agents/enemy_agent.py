from Interfaces.IBDI_Agent import IBDI_Agent

class Enemy_Agent(IBDI_Agent):
    """
    Um agente que representa um personagem inimigo com lógica BDI.
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
   
    def update_desires(self):
        pass

    def deliberate(self):
        pass

    def execute_plan(self):
        pass

    def step(self):
        print("-"*40)
        print(f"Executando step do animal...")
        print(f'INBOX: {self.inbox}')
        # self.process_message()
        self.update_desires()
        self.deliberate()
        self.execute_plan()
        print(f'INTENÇÃO [{self.unique_id}]: {self.intention}')        
        print(f'CRENÇAS [{self.unique_id}]: {self.beliefs}')        
        print("-"*40)