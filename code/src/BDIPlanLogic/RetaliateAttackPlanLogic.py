from BDIPlanLogic.beliefs_tree import (
    DecisionTree, 
    DecisionNode, 
    IntentionNode
    )
from utils.get_distance import get_distance

class RetaliateAttackPlanLogic:
    """
    Esta classe encapsula a lógica de decisão para um agente
    que foi atacado (Retaliate Attack).
    """
    
    def __init__(self):
        # 1. Funções de Condição (Consultas às Crenças)
        
        def cond_foi_atacado(agent):
            """RAIZ: "Foi atacado?" """
            return agent.beliefs.get('received_attack') is not None

        def cond_possui_alvo(agent):
            """Nó 1.1: "Possui alvo?" """
            return agent.beliefs.get('target') is not None
        
        def cond_consegue_atacar(agent):
            """Nó 1.1.1: "Consegue atacar o alvo de onde está?" """
            if agent.beliefs.get('target') is None or agent.cell is None:
                return False
            
            try:
                distance = get_distance(
                    x1=agent.cell.coordinate[0],
                    y1=agent.cell.coordinate[1],
                    x2=agent.beliefs['target'].cell.coordinate[0],
                    y2=agent.beliefs['target'].cell.coordinate[1],
                    )
            except Exception:
                return False 

            if distance is None:
                return False
            return agent.beliefs['range'] >= distance-2
        
        # 2. Construir a árvore e armazenar o "motor"
        raiz = self._build_tree(
            cond_foi_atacado,
            cond_possui_alvo,
            cond_consegue_atacar
        )
        self.decision_tree = DecisionTree(root=raiz)

    def _build_tree(self, cond_foi_atacado, cond_possui_alvo, cond_consegue_atacar):
        # --- PASSO A: Definir todas as FOLHAS (Ações) ---
        acao_continuar = IntentionNode("CONTINUAR")
        acao_definir_alvo = IntentionNode("DEFINIR ALVO")
        acao_atacar = IntentionNode("ATACAR")
        acao_aproximar = IntentionNode("APROXIMAR-SE")
        # --- PASSO B: Construir os RAMOS (de baixo para cima) ---
        
        # Nó 1.1.1: "Consegue atacar...?"
        ramo_consegue_atacar = DecisionNode(
            condition_func=cond_consegue_atacar,
            yes_node=acao_atacar,
            no_node=acao_aproximar
        )

        # Nó 1.1: "Possui alvo?"
        ramo_possui_alvo = DecisionNode(
            condition_func=cond_possui_alvo,
            yes_node=ramo_consegue_atacar,  
            no_node=acao_definir_alvo
        )
        
        # RAIZ: "Foi atacado?"
        raiz = DecisionNode(
            condition_func=cond_foi_atacado,
            yes_node=ramo_possui_alvo,      
            no_node=acao_continuar
        )
        
        return raiz

    def get_intention(self, agent):
        """Interface pública para o agente BDI."""
        return self.decision_tree.decide(agent)