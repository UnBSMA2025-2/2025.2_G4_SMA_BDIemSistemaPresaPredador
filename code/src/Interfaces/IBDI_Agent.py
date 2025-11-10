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
        self.beliefs = {}
        
        # 2. Desejos (Desires): Os objetivos de alto nível do agente.
        self.desires = set()
        
        # 3. Intenções (Intentions): O plano ou ação que o agente 
        self.intention = None

    # --- Métodos Abstratos (Ciclo BDI) ---

    @abc.abstractmethod
    def update_desires(self):
        """
        Fase 1 do BDI: Atualizar desejos).
        """
        pass

    @abc.abstractmethod
    def deliberate(self):
        """
        Fase 2 do BDI: Deliberar (Deliberate).
        """
        pass

    @abc.abstractmethod
    def execute_plan(self):
        """
        Fase 3 do BDI: Agir (Act / Execute Plan).
        """
        pass

    @abc.abstractmethod
    def step(self):
        """
        Método 'step' do MESA.
        """
        pass