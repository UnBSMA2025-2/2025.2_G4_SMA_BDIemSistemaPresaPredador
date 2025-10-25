from Interfaces.IBDI_Agent import IBDI_Agent

class Enemy_Agent(IBDI_Agent):
    """
    Um agente que representa um personagem inimigo com lógica BDI.
    """
    def __init__(self, model, life, defense, nome="Animal"):
        # Inicializa a interface IBDI_Agent (que inicializa mesa.Agent)
        super().__init__(model)
        
        # --- Atributos Básicos do RPG ---
        self.nome = nome
        self.life = life
        self.defense = defense
        self.is_alive = True if self.life > 0 else False

        self.beliefs['my_health'] = self.life
        self.beliefs['my_stats'] = {
            'defense': self.defense
        }

    def process_messages(self, messages):
        """
        Processa uma lista de mensagens recebidas.
        """
        print(f"  > Agente {self.unique_id} ({self.nome}): Processando {len(messages)} mensagem(ns)...")
        
        for msg in messages:
            sender = msg['sender']
            content = msg['content']
            
            if content['type'] == 'attack':
                attack_power = content['value']
                print(f"  > Agente {self.unique_id} ({self.nome}): Recebi um ataque de {sender} com poder {attack_power}.")
                
                # Cálculo do dano (Ataque - Defesa)
                damage_taken = attack_power - self.defense
                
                # Garante que o dano não seja negativo
                if damage_taken < 0:
                    damage_taken = 0
                
                print(f"  > Agente {self.unique_id} ({self.nome}): Meu HP era {self.life}. Sofri {damage_taken} de dano (Defesa: {self.defense}).")
                self.life -= damage_taken
                
                if self.life <= 0:
                    self.is_alive = False
                    print(f"  > Agente {self.unique_id} ({self.nome}): Fui derrotado!")
            else:
                print(f"  > Agente {self.unique_id} ({self.nome}): Recebi mensagem desconhecida de {sender}: {content['type']}")

    def introduce_yourself(self):
        print(f"--- Apresentação do inimigo: {self.unique_id} ({self.nome}) ---")
        if self.is_alive:
            print(f"  Vida: {self.life}")
        else:
            print("  Status: Derrotado.")
        print("-" * (20 + len(self.nome) + len(str(self.unique_id))))
    
    def update_beliefs(self):
        """ 
        Fase 1 do BDI: Perceber.
        Atualiza crenças internas (saúde) e percebe o ambiente (mensagens).
        """
        # 1. Perceber estado interno
        self.beliefs['my_health'] = self.life
        
        # 2. Perceber ambiente externo (Checar "Correio")
        mensagens_recebidas = self.model.get_messages(self.unique_id)
        
        if mensagens_recebidas:
            # Se houver mensagens, processa-as
            self.process_messages(mensagens_recebidas)
            
        # 3. Atualizar estado de vida (após processar dano)
        if self.life <= 0 and self.is_alive:
            self.is_alive = False
            self.beliefs['my_health'] = 0

    def deliberate(self):
        pass

    def execute_plan(self):
        pass

    def step(self):
        print(f"Executando step do animal...")
        self.update_beliefs()
        # self.deliberate()
        # self.execute_plan()