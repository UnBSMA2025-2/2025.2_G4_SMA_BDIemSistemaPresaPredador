from BDIPlanLogic.beliefs_tree import (
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
        # Funções de condição (consultam crenças do agente)
        def cond_agent_half_hp_and_not_in_battle(agent):
            """Condição Raiz: hp > 50% e não está em batalha"""
            return agent.beliefs['hp'] > (agent.beliefs['hpMax'] * 0.5) and not agent.beliefs.get('em_batalha', False)

        def cond_healing_item_nearby(agent):
            """Há item de cura ao lado? Salva coordenada se sim."""
            healing_cells = agent.cell.get_neighborhood(agent.beliefs['displacement']).cells
            for cell in healing_cells:
                if cell.beliefs.get('healing_item_spot', False):
                    agent.beliefs['healing_item_spot'] = cell.coordinate
                    return True
            return False

        def cond_healing_item_in_range(agent):
            """Há item de cura em algum lugar do grid? Salva coordenada se sim."""
            for cell in agent.model.grid.coord_iter():
                _, x, y = cell
                if agent.model.grid[x][y].beliefs.get('healing_item_spot', False):
                    agent.beliefs['healing_item_spot'] = (x, y)
                    return True
            return False

        def cond_enemy_nearby(agent):
            """Há inimigos por perto?"""
            enemy_cells = agent.cell.get_neighborhood(agent.beliefs['displacement'])
            for cell in enemy_cells:
                if not cell.is_empty:
                    for a in cell.agents:
                        if a.type == 'ANIMAL':
                            return True
            return False

        # Construir a árvore de decisão
        raiz = self._build_tree(
            cond_agent_half_hp_and_not_in_battle,
            cond_healing_item_nearby,
            cond_healing_item_in_range,
            cond_enemy_nearby,
        )
        self.decision_tree = DecisionTree(raiz)

    def _build_tree(
        self,
        cond_agent_half_hp_and_not_in_battle,
        cond_healing_item_nearby,
        cond_healing_item_in_range,
        cond_enemy_nearby):
        """
        Constrói a árvore de decisão para exploração
        """
        # Folhas (ações)
        acao_adquirir_item = IntentionNode('ADQUIRIR ITEM')
        acao_aproximar_item = IntentionNode('APROXIMAR DO ITEM')
        acao_explorar_mapa = IntentionNode('EXPLORAR')
        acao_definir_alvo = IntentionNode('DEFINIR ALVO')

        # Ramos
        healing_item_in_range = DecisionNode(
            condition_func=cond_healing_item_in_range,
            yes_node=acao_aproximar_item,
            no_node=acao_explorar_mapa
        )

        healing_item_nearby = DecisionNode(
            condition_func=cond_healing_item_nearby,
            yes_node=acao_adquirir_item,
            no_node=healing_item_in_range
        )

        enemy_nearby = DecisionNode(
            condition_func=cond_enemy_nearby,
            yes_node=acao_definir_alvo,
            no_node=acao_explorar_mapa
        )

        raiz = DecisionNode(
            condition_func=cond_agent_half_hp_and_not_in_battle,
            yes_node=healing_item_nearby,
            no_node=enemy_nearby
        )
        return raiz

    def get_intention(self, agent):
        """Interface pública para o agente BDI."""
        return self.decision_tree.decide(agent)