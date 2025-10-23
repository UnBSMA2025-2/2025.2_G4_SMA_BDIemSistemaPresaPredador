import mesa
import RPGAgent

class RPGModel(mesa.Model):
    """
    Modelo MESA para simular o mundo do RPG.
    """
    
    def __init__(self, seed=None, n=1, some_kwarg_I_need=True):
        """
        Inicializa o modelo, o scheduler e cria o agente único.
        """
        super().__init__(seed=seed)        
        
        agent_nome="Marllon" 
        agent_life = 10 
        agent_attack = 20 
        agent_defense = 30
        self.num_agents = n

        agents = RPGAgent.create_agents(
            model=self,
            n=1,
            life=agent_life,
            attack=agent_attack,
            defense=agent_defense,
            nome=agent_nome
        )

    def step(self):
        """
        Define o que acontece em um "passo" (tick) da simulação.
        """
        print("\n--- Início do Passo da Simulação (Model.step()) ---")
        print(f"Modelo: Criando agente...")
        
        self.agents.shuffle_do("step")
                
        print("--- Fim do Passo da Simulação ---")