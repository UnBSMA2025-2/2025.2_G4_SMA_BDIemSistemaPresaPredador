import mesa
from collections import defaultdict
from mesa.discrete_space import OrthogonalMooreGrid
from Agents.character_agent import Character_Agent 
from Agents.enemy_agent import Enemy_Agent 
from mocks.beliefs import beliefs1, beliefs2, beliefs3
from communication import MessageDict


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

    def send_message(self, message:MessageDict):
        """
        Método público para qualquer agente enviar uma mensagem.
        O modelo armazena a mensagem na caixa do destinatário.
        """
        print(self.message_box)
        # Se o destinatário ainda não tem uma lista de mensagens, cria uma
        if message['receiver'] not in self.message_box:
            self.message_box[message['receiver']] = []
        
        self.message_box[message['receiver']].append(message)

    def get_messages(self, recipient_id):
        """
        Método para um agente resgatar suas mensagens.
        Retorna a lista de mensagens e limpa a caixa de entrada 
        daquele agente.
        """
        if recipient_id in self.message_box:
            messages = self.message_box.pop(recipient_id) 
            print(messages)
            return messages
        
        # Nenhuma mensagem para este agente
        return []

    def step(self):
        print("\n" + "="*40)
        print(f"--- Início do Passo {self.steps} da Simulação ---")

        self.message_box = {}
        
        self.agents.shuffle_do("step")
        
        print("="*40)