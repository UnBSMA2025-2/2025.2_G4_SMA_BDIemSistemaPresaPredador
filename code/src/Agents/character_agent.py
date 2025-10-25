from Interfaces.IBDI_Agent import IBDI_Agent

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

    def introduce_yourself(self):
        print(f"--- Apresentação do personagem: {self.unique_id} ({self.nome}) ---")
        if self.is_alive:
            print(f"  Vida: {self.life}")
            print(f"  Ataque: {self.attack}")
            print(f"  Defesa: {self.defense}")
        else:
            print("  Status: Derrotado.")
        print("-" * (20 + len(self.nome) + len(str(self.unique_id))))

    def attack_target(self, recipient_id):
        """
        (Novo Comportamento - Ação de Envio)
        Envia uma mensagem contendo o valor de ataque do agente
        para um destinatário específico, usando o "Correio" do modelo.
        """
        print(f"  > Agente {self.unique_id} ({self.nome}): Estou enviando meu status de ataque ({self.attack}) para o agente {recipient_id}.")
        
        # 1. Define o conteúdo da mensagem
        message_content = {
            'type': 'attack',  # Tipo da mensagem
            'value': self.attack       # O dado da mensagem
        }
        # 2. Chama o método do modelo para "postar" a mensagem
        self.model.send_message(
            sender_id=self.unique_id,
            recipient_id=recipient_id,
            content=message_content
        )
    
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
        print(f"Executando step do personagem...")
        self.update_beliefs()
        # self.deliberate()
        # self.execute_plan()