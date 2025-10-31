from Beliefs.beliefs_tree import (
    DecisionTree, 
    DecisionNode, 
    IntentionNode
    )

class ExplorationPlanLogic:
    """
    Esta classe encapsula a lógica de decisão para um agente
    em situações de exploração.
    """
    
    def __init__(self):
        # 1. Funções de Condição (Consultas às Crenças)
        #    Estas funções leem o dicionário 'context' (crenças)
        
        def cond_agent_half_hp(agent):
            """Condição 1: agente.hp < 50% ?"""
            return agent.beliefs['hp'] < agent.beliefs['hpMax']*(0.5)
        
        def cond_heal_in_range(agent):
            """Condição 1.1: há cura por perto? - verifica células próximas"""
            healing_cells = agent.model.grid.get_cells_in_range(
                center=agent.cell.coordinate,
                range_distance=agent.beliefs['displacement']
            )
            for cell in healing_cells:
                if cell.beliefs['healing_spot']:
                    return True
            return False
        
        def cond_enemy_in_range(agent):
            """Condição 1.2: há um inimigo por perto? - verifica células próximas"""
            enemy_cells = agent.model.grid.get_cells_in_range(
                center=agent.cell.coordinate,
                range_distance=agent.beliefs['displacement']
            )
            for cell in enemy_cells:
                if not cell.is_empty: # se há algo na célula
                    for a in cell.agents:
                        if a.type == 'COMMON_ENEMY': # se for um inimigo comum
                            return True
            return False

        # 2. Construir a árvore e armazenar o "motor"
        raiz = self.build_tree(
            cond_agent_half_hp,
            cond_heal_in_range,
            cond_enemy_in_range,
        )
        self.decision_tree = DecisionTree(raiz)

        def build_tree(self, cond_agent_half_hp, cond_heal_in_range, cond_enemy_in_range):
            # Nó folha: Ações/Intenções
            acao_adquirir_cura = IntentionNode('ADQUIRIR CURA')
            acao_explorar = IntentionNode('EXPLORAR')
            acao_definir_alvo_inimigo = IntentionNode('DEFINIR ALVO INIMIGO')

            # Nós de decisão
            heal_in_range = DecisionNode(
                condition_func=cond_heal_in_range,
                yes_node=acao_adquirir_cura,
                no_node=acao_explorar
            )

            enemy_in_range = DecisionNode(
                condition_func=cond_enemy_in_range,
                yes_node=acao_definir_alvo_inimigo,
                no_node=acao_explorar
            )

            raiz = DecisionNode(
                condition_func=cond_agent_half_hp,
                yes_node=heal_in_range,
                no_node=enemy_in_range
            )

            return raiz
        
    def get_intention(self, agent):
        """Interface pública para o agente BDI."""
        return self.decision_tree.decide(agent)