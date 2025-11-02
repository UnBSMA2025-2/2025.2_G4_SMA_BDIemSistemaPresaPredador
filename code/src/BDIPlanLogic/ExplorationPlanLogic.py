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
        
        def cond_agent_half_hp_and_not_in_battle(agent):
            """Condição Raiz: agent.hp > 50% and not em_batalha ?"""
            print(agent.beliefs['hp'] > (agent.beliefs['hpMax'] * 0.5) and not agent.beliefs['em_batalha'])
            return agent.beliefs['hp'] > (agent.beliefs['hpMax'] * 0.5) and not agent.beliefs['em_batalha']

        def cond_healing_item_nearby(agent):
            """Condição: Há item de cura ao lado? - verifica células próximas"""
            healing_cells = agent.cell.get_neighborhood(
                agent.beliefs['displacement']
            ).cells
            for cell in healing_cells:
                if cell.beliefs.get('healing_item_spot', False):
                    agent.beliefs['healing_item_spot'] = cell.coordinate
                    print('há item de cura ao lado?')
                    return True
            return False

        def cond_healing_item_in_range(agent):
            """Condição: Há item de cura em algum lugar do grid?"""
            print('há item de cura em algum lugar do grid?')
            for cell in agent.model.grid.coord_iter():
                _, x, y = cell
                if agent.model.grid[x][y].beliefs.get('healing_item_spot', False):
                    agent.beliefs['healing_item_spot'] = (x, y)
                    return True
            return False
            
        def cond_enemy_nearby(agent):
            """Condição: há inimigos por perto? - verifica células próximas"""

            enemy_cells = agent.cell.get_neighborhood(
                agent.beliefs['displacement']
            )

            for cell in enemy_cells:
                if not cell.is_empty:
                    for a in cell.agents:
                        # TO-DO : ajustar tipo de inimigo conforme modelo
                        if a.type == 'ANIMAL':
                            return True
            return False

        # 2. Construir a árvore e armazenar o "motor"
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
        Constrói a árvore de decisão...
        """
        
        # --- PASSO A: Definir todas as FOLHAS (Ações) ---
        acao_adquirir_item = IntentionNode('ADQUIRIR ITEM')
        acao_aproximar_item = IntentionNode('APROXIMAR DO ITEM')
        acao_explorar_mapa = IntentionNode('EXPLORAR')
        acao_definir_alvo = IntentionNode('DEFINIR ALVO')

         # --- PASSO B: Construir os RAMOS (de baixo para cima) ---

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