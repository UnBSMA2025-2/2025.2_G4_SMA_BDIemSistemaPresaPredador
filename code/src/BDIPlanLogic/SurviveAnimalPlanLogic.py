from BDIPlanLogic.beliefs_tree import (
    DecisionTree, 
    DecisionNode, 
    IntentionNode
    )
from utils.get_distance import get_distance

class SurviveAnimalPlanLogic:
    """
    Esta classe encapsula a lógica de decisão para um agente
    em situações de sobrevivência.
    """
    
    def __init__(self):
        # 1. Funções de Condição (Consultas às Crenças)
        #    Estas funções leem o dicionário 'context' (crenças)

        def cond_other_agents_nearby(agent):
            vizinhos = agent.cell.neighborhood
            for cell in vizinhos:
                if len(cell.agents) != 0:
                    return True
            return False
        
        def cond_other_animal_nearby(agent):
            vizinhos = agent.cell.neighborhood
            for cell in vizinhos:
                if len(cell.agents) != 0:
                    if cell.agents[0].type != 'ANIMAL':
                        return True
            return False

        # 2. Construir a árvore e armazenar o "motor"
        raiz = self._build_tree(
            cond_other_agents_nearby,
            cond_other_animal_nearby,
        )
        self.decision_tree = DecisionTree(root=raiz)

    def _build_tree(self, cond_other_agents_nearby, cond_other_animal_nearby):
        """
        Constrói a árvore de decisão de "baixo para cima",
        baseado no rascunho.
        """
        
        # --- PASSO A: Definir todas as FOLHAS (Ações) ---
        acao_fugir = IntentionNode("FUGIR")
        acao_esperar = IntentionNode("EXPLORAR")
        acao_aproximar = IntentionNode("APROXIMAR-SE")
        # --- PASSO B: Construir os RAMOS (de baixo para cima) ---
                
        ramo_1_1 = DecisionNode(
            condition_func=cond_other_animal_nearby,
            yes_node=acao_fugir, 
            no_node=acao_aproximar
        )
        
        raiz = DecisionNode(
            condition_func=cond_other_agents_nearby,
            yes_node=ramo_1_1,     
            no_node=acao_esperar        
        )
        
        return raiz

    def get_intention(self, agent):
        """Interface pública para o agente BDI."""
        return self.decision_tree.decide(agent)