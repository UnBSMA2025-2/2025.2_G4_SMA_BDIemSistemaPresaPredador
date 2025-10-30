import mesa
from mesa.discrete_space import OrthogonalMooreGrid
from Agents.character_agent import Character_Agent 
from Agents.enemy_agent import Enemy_Agent 
from mocks.beliefs import beliefs1, beliefs2, beliefs3

class RPGModel(mesa.Model):
    """
    Modelo MESA para simular o mundo do RPG.
    """
    
    def __init__(self, width=10, height=10, seed=None, n=5, some_kwarg_I_need=True):
        """
        Inicializa o modelo, o scheduler e cria o agente único.
        """
        super().__init__(seed=seed)
        self.message_box = {}
        self.num_agents = n
        self.grid = OrthogonalMooreGrid(
            (width, height), torus=True, capacity=1, random=self.random
        )
        
        Character_Agent.create_agents(
            model=self,
            cell=self.grid.all_cells.cells[0],
            n=self.num_agents,
            beliefs=beliefs3
        )
        Character_Agent.create_agents(
            model=self,
            cell=self.grid.all_cells.cells[4],
            n=self.num_agents,
            beliefs=beliefs2
        )
        Character_Agent.create_agents(
            model=self,
            cell=self.grid.all_cells.cells[24],
            n=self.num_agents,
            beliefs=beliefs2
        )

        agent1 = next(iter(self.agents.select(
            lambda agent: agent.unique_id == 1
        )))
        agent2 = next(iter(self.agents.select(
            lambda agent: agent.unique_id == 2
        )))

        agent1.beliefs['target'] = agent2
        agent2.beliefs['target'] = agent1

    def send_message(self, sender_id, recipient_id, content):
        """
        Método público para qualquer agente enviar uma mensagem.
        O modelo armazena a mensagem na caixa do destinatário.
        """
        # Se o destinatário ainda não tem uma lista de mensagens, cria uma
        if recipient_id not in self.message_box:
            self.message_box[recipient_id] = []
            
        message = {
            'sender': sender_id,
            'content': content
        }
        
        self.message_box[recipient_id].append(message)
        print(f"[Modelo (Correio)]: Mensagem de {sender_id} para {recipient_id} registrada.")

    def get_messages(self, recipient_id):
        """
        Método para um agente "puxar" (pull) suas mensagens.
        Retorna a lista de mensagens e limpa a caixa de entrada 
        daquele agente.
        """
        if recipient_id in self.message_box:
            # Pega as mensagens (.pop() remove a chave do dicionário)
            messages = self.message_box.pop(recipient_id) 
            print(f"[Modelo (Correio)]: Agente {recipient_id} coletou {len(messages)} mensagem(ns).")
            return messages
        
        # Nenhuma mensagem para este agente
        return []

    def step(self):
        """
        Define o que acontece em um "passo" (tick) da simulação.
        """
        print("\n" + "="*40)
        print(f"--- Início do Passo {self.steps} da Simulação ---")

        self.message_box = {}
        
        self.agents.shuffle_do("step")
        
        print("="*40)