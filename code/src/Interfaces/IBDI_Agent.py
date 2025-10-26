import abc
from mesa.discrete_space import CellAgent 

class IBDI_Agent(CellAgent, abc.ABC):
    """
    Interface (Classe Base Abstrata) para Agentes com arquitetura BDI.
    
    Esta classe define o contrato que todos os agentes BDI devem seguir. 
    Ela garante que os três componentes principais (Crenças, Desejos, 
    Intenções) estejam presentes e que o ciclo de deliberação (perceber, 
    pensar, agir) seja implementável.
    """
    
    def __init__(self, model):
        """
        Inicializa os componentes BDI.
        """
        super().__init__(model)
        
        # 1. Crenças (Beliefs): O que o agente "sabe" ou "acredita"
        #    (Deve ser inicializado pela classe filha, tipicamente como dict)
        self.beliefs = {}
        
        # 2. Desejos (Desires): Os objetivos de alto nível do agente.
        #    (Deve ser inicializado pela classe filha, tipicamente como set)
        self.desires = set()
        
        # 3. Intenções (Intentions): O plano ou ação que o agente 
        #    (Deve ser inicializado pela classe filha, tipicamente como None)
        self.intention = None

    # --- Métodos Abstratos (Ciclo BDI) ---

    @abc.abstractmethod
    def update_beliefs(self):
        """
        Fase 1 do BDI: Perceber (Sense).
        
        O agente deve coletar informações do ambiente e atualizar seu estado 
        interno (self.beliefs).
        """
        pass

    @abc.abstractmethod
    def deliberate(self):
        """
        Fase 2 do BDI: Deliberar (Deliberate).
        
        O agente deve avaliar suas crenças (self.beliefs) contra seus
        desejos (self.desires) para selecionar uma intenção 
        (self.intention) a ser executada.
        """
        pass

    @abc.abstractmethod
    def execute_plan(self):
        """
        Fase 3 do BDI: Agir (Act / Execute Plan).
        
        O agente deve executar a ação concreta no ambiente (modificar 
        o 'model' ou 'grid') com base na intenção (self.intention) 
        definida na fase de deliberação.
        """
        pass

    @abc.abstractmethod
    def step(self):
        """
        Método 'step' do MESA.
        
        Este método é chamado pelo scheduler do MESA a cada passo.
        Ele deve orquestrar a execução do ciclo BDI, tipicamente
        chamando:
        
        1. self.update_beliefs()
        2. self.deliberate()
        3. self.execute_plan()
        """
        pass