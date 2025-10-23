import IBDI_Agent

class Character_Agent(IBDI_Agent):
    """
    Um agente que representa um personagem de RPG com lógica BDI.
    """
    def __init__(self, model, life, attack, defense, nome="Personagem"):
        # Inicializa a interface IBDI_Agent (que inicializa mesa.Agent)
        super().__init__(model)
        
        # --- Atributos Básicos do RPG ---
        self.nome = nome
        self.life = life
        self.attack = attack
        self.defense = defense
        self.is_alive = True if self.life > 0 else False

        self.beliefs['my_health'] = self.life
        self.beliefs['my_stats'] = {
            'attack': self.attack,
            'defense': self.defense
        }

    def se_apresentar(self):
        print(f"--- Apresentação do Agente {self.unique_id} ({self.nome}) ---")
        if self.is_alive:
            print(f"  Vida: {self.life}")
            print(f"  Ataque: {self.attack}")
            print(f"  Defesa: {self.defense}")
        else:
            print("  Status: Derrotado.")
        print("-" * (20 + len(self.nome) + len(str(self.unique_id))))
    
    def update_beliefs(self):
        """ 
        Atualiza as crenças do agente sobre o mundo.
        """
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