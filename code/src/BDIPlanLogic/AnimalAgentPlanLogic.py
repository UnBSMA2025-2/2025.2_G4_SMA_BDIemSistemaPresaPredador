from BDIPlanLogic.beliefs_tree import (
    DecisionTree,
    DecisionNode,
    IntentionNode
)

class AnimalAgentPlanLogic:
    """
    Esta classe encapsula a lógica de decisão para um agente inimigo
    """
    
    def __init__(self):
        def cond_in_battle(agent):
            return agent.beliefs['em_batalha']
        
        def cond_low_hp(agent):
            cur_hp = (agent.beliefs['hp'] / agent.beliefs['hpMax']) 
            return cur_hp < 0.2
        
        def cond_hp_not_full(agent):
            return agent.beliefs['hp'] < agent.beliefs['hpMax']
        
        raiz = self._build_tree(
            cond_in_battle,
            cond_low_hp,
            cond_hp_not_full
        )
        
        self.decision_tree = DecisionTree(root=raiz)
        
    def _build_tree(self, cond_in_battle, cond_low_hp, cond_hp_not_full):
        acao_fugir = IntentionNode('FUGIR')
        acao_desesperar = IntentionNode('DESESPERAR')
        acao_curar = IntentionNode('CURAR')
        acao_explorar = IntentionNode('EXPLORAR')
        
        ramo_1_2 = DecisionNode(
            condition_func=cond_hp_not_full,
            yes_node=acao_curar,
            no_node=acao_explorar
        )
        
        ramo_1_1 = DecisionNode(
            condition_func=cond_low_hp,
            yes_node=acao_desesperar,
            no_node=acao_fugir
        )
        
        raiz = DecisionNode(
            condition_func=cond_in_battle,
            yes_node=ramo_1_1,
            no_node=ramo_1_2
        )
        
        return raiz
    
    def get_intention(self, agent):
        return self.decision_tree.decide(agent)