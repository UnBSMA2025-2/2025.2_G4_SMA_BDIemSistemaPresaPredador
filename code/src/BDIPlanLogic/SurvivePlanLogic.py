from BDIPlanLogic.beliefs_tree import (
    DecisionTree, 
    DecisionNode, 
    IntentionNode
    )
from utils.get_distance import get_distance

class SurvivePlanLogic:
    """
    Esta classe encapsula a lógica de decisão para um agente
    em situações de sobrevivência.
    """
    
    def __init__(self):
        # 1. Funções de Condição (Consultas às Crenças)
        #    Estas funções leem o dicionário 'context' (crenças)
        
        def cond_in_battle(agent):
            """Condição 1: em_batalha == true ?"""
            return agent.beliefs['em_batalha']
        
        def cond_target_low_hp(agent):
            """Condição 1.1: agente_alvo.hp < 10% ?"""
            if agent.beliefs['target'] is None:
                return False # Não pode ter HP baixo se não há alvo
            return agent.beliefs['target'].beliefs['hp'] < agent.beliefs['target'].beliefs['hpMax']*(0.1)
        
        def cond_have_healing(agent):
            return agent.beliefs['num_healing'] > 1
        
        def cond_distance(agent):
            if agent.beliefs['target'] is not None and agent.cell is not None and agent.beliefs['target'].cell is not None:
                distance = get_distance(
                    x1=agent.cell.coordinate[0],
                    y1=agent.cell.coordinate[1],
                    x2=agent.beliefs['target'].cell.coordinate[0],
                    y2=agent.beliefs['target'].cell.coordinate[1],
                    )
                return distance == 1
            return False
        
        def cond_friend_free(agent):
            if len(agent.get_friends()) == 0:
                return False
            return not agent.get_friends()[0].agents[0].beliefs['em_batalha']
        
        def cond_friend_distance(agent):
            distance = get_distance(
                x1=agent.cell.coordinate[0],
                y1=agent.cell.coordinate[1],
                x2=agent.get_friends()[0].agents[0].cell.coordinate[0],
                y2=agent.get_friends()[0].agents[0].cell.coordinate[1],
                )

            if distance is None:
                return False # Se não sei a distância, não posso atacar
            return distance == 1

        # 2. Construir a árvore e armazenar o "motor"
        raiz = self._build_tree(
            cond_in_battle,
            cond_target_low_hp,
            cond_have_healing,
            cond_distance,
            cond_friend_free,
            cond_friend_distance,
        )
        self.decision_tree = DecisionTree(root=raiz)

    def _build_tree(self, cond_in_battle, cond_target_low_hp, cond_have_healing, cond_distance, cond_friend_free, cond_friend_distance,):
        """
        Constrói a árvore de decisão de "baixo para cima",
        baseado no rascunho.
        """
        
        # --- PASSO A: Definir todas as FOLHAS (Ações) ---
        acao_atacar = IntentionNode("ATACAR INIMIGO")
        acao_curar = IntentionNode("CURAR")
        acao_fugir = IntentionNode("FUGIR")
        acao_aproximar = IntentionNode("APROXIMAR-SE")
        acao_aproximar_de_amigo = IntentionNode("APROXIMAR-SE DE AMIGO")
        acao_obter_cura = IntentionNode("OBTER CURA")
        acao_esperar = IntentionNode("ESPERAR")
        
        # --- PASSO B: Construir os RAMOS (de baixo para cima) ---
        
        # O que fazer se (em_batalha=S) e (alvo_hp_baixo=N)
        ramo_1_1_2 = DecisionNode(
            condition_func=cond_have_healing,
            yes_node=acao_curar,   
            no_node=acao_fugir     
        )

        ramo_1_2_2_1 = DecisionNode(
            condition_func=cond_friend_distance,
            yes_node=acao_obter_cura,
            no_node=acao_aproximar_de_amigo)

        ramo_1_2_2 = DecisionNode(
            condition_func=cond_friend_free,
            yes_node=ramo_1_2_2_1,
            no_node=acao_esperar)

        ramo_1_2 = DecisionNode(
            condition_func=cond_have_healing,
            yes_node=acao_curar,  
            no_node=ramo_1_2_2    
        )

        ramo_1_1_1 = DecisionNode(
            condition_func=cond_distance,
            yes_node=acao_atacar,        
            no_node=acao_aproximar       
        )
        
        ramo_1_1 = DecisionNode(
            condition_func=cond_target_low_hp,
            yes_node=ramo_1_1_1, 
            no_node=ramo_1_1_2
        )
        
        raiz = DecisionNode(
            condition_func=cond_in_battle,
            yes_node=ramo_1_1,     
            no_node=ramo_1_2        
        )
        
        return raiz

    def get_intention(self, agent):
        """Interface pública para o agente BDI."""
        return self.decision_tree.decide(agent)