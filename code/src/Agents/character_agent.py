from Interfaces.IBDI_Agent import IBDI_Agent
from utils.find_nearest_position import move_to_agent

class Character_Agent(IBDI_Agent):
    """
    Um agente que representa um personagem de RPG com lógica BDI.
    """
    def __init__(self, model, cell, life, attack, defense, nome="Personagem", displacement=3):
        # Inicializa a interface IBDI_Agent (que inicializa mesa.Agent)
        super().__init__(model)
        
        self.cell = cell
        
        # --- Atributos Básicos do RPG ---
        self.nome = nome
        self.life = life
        self.attack = attack
        self.defense = defense
        self.displacement = displacement
        self.is_alive = True if self.life > 0 else False

        self.beliefs['my_health'] = self.life
        self.beliefs['my_stats'] = {
            'attack': self.attack,
            'defense': self.defense
        }

    def move_to_target(self, target_coordinate=(0,0), h=10, l=10):
        pos_a = self.cell.coordinate
        pos_b = target_coordinate
        
        new_position = move_to_agent(
            h, 
            l, 
            pos_a[0],
            pos_a[1],
            pos_b[0], 
            pos_b[1], 
            self.displacement
        )
        
        new_cell = next(iter(self.model.grid.all_cells.select(
            lambda cell: cell.coordinate == new_position
        )))
        
        if new_cell.is_empty:
            self.cell = new_cell
        else:
            if target_coordinate[0] == 0: return self.move_to_target(
                (target_coordinate[0]+1, target_coordinate[1]), h, l
            )
            elif target_coordinate[0] == h: return self.move_to_target(
                (target_coordinate[0]-1, target_coordinate[1]), h, l
            )
            elif target_coordinate[1] == 0: return self.move_to_target(
                (target_coordinate[0], target_coordinate[1]+1), h, l
            )
            elif target_coordinate[1] == l: return self.move_to_target(
                (target_coordinate[0], target_coordinate[1]-1), h, l
            )

    def introduce_yourself(self):
        print(f"--- Apresentação do personagem: {self.unique_id} ({self.nome}) ---")
        if self.is_alive:
            print(f"  Vida: {self.life}")
            print(f"  Ataque: {self.attack}")
            print(f"  Defesa: {self.defense}")
            print(f"  Posição: {self.cell}")
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