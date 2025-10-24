import mesa
from Agents.character_agent import Character_Agent 
from Agents.enemy_agent import MOBAgent 

class RPGModel(mesa.Model):
    """
    Modelo MESA para simular o mundo do RPG.
    """
    
    def __init__(self, seed=None, n=1, some_kwarg_I_need=True):
        """
        Inicializa o modelo, o scheduler e cria o agente único.
        """
        super().__init__(seed=seed)
        
        Character_Agent.create_agents(
            model=self,
            n=1,
            life=10,
            attack=20,
            defense=30,
            nome="Marllon" 
        )
        MOBAgent.create_agents(
            model=self,
            n=1,
            life=5,
            defense=15,
            nome="Lobo"
        )

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

    def step(self):
        """
        Define o que acontece em um "passo" (tick) da simulação.
        """
        print("\n" + "="*40)
        print(f"--- Início do Passo {self.steps} da Simulação ---")

        self.message_box = {}
        self.agents.shuffle_do("step")

        def getAgentById(agents, agent_id):
            for agent in agents:
                if agent.unique_id == agent_id:
                    return agent
            return null

        agente1 = next(iter(self.agents.select(
            lambda agent: agent.unique_id == 1 
        )))
        
        # print(f"Agente do self.agents.select(): {agente1.nome}")
        
        print(f"[Modelo (Orquestrador)]: Acionando Grog (ID 1) para enviar status ao Lobo (ID 2)...")
        agente1.enviar_status_ataque(recipient_id=2)
        
        print(f"[Modelo (Correio)]: Status final da 'message_box': {self.message_box}")

        print(f"--- Fim do Passo {self.steps} da Simulação ---")
        print("="*40)