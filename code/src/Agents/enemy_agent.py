import IBDI_Agent

class MOBAgent(IBDI_Agent):
    """
    Um agente que representa um personagem inimigo com lógica BDI.
    """
    def __init__(self, model, life, nome="Animal"):
        super().__init__(model)
        
        self.nome = nome
        self.life = life
        self.is_alive = True if self.life > 0 else False

        self.beliefs['my_health'] = self.life
        self.beliefs['my_stats'] = {}

    def se_apresentar(self):
        print(f"--- Apresentação do inimigo: {self.unique_id} ({self.nome}) ---")
        if self.is_alive:
            print(f"  Vida: {self.life}")
        else:
            print("  Status: Derrotado.")
        print("-" * (20 + len(self.nome) + len(str(self.unique_id))))
    
    def update_beliefs(self):
        self.beliefs['my_health'] = self.life
        if self.life <= 0 and self.is_alive:
            self.is_alive = False

    def deliberate(self):
        pass

    def execute_plan(self):
        pass

    def step(self):
        self.update_beliefs()
        self.se_apresentar()
        # self.deliberate()
        # self.execute_plan()