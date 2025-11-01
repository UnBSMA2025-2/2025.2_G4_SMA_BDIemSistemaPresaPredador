from Beliefs.beliefs_tree import (
    DecisionTree, 
    DecisionNode, 
    IntentionNode
    )
from utils.get_distance import get_distance

class BattlePlanLogic:
    
    def __init__(self):
        
        def cond_has_target(agent):
            """Condição Raiz: O agente tem um alvo?"""
            return agent.beliefs.get('em_batalha')
        
        def cond_enable_atk_enemy(agent):
            range = agent.beliefs['range']
            pos = agent.cell.coordinate
            enemy = agent.beliefs['target']
            enemy_pos = enemy.cell.coordinate
            d = get_distance(pos[0], pos[1], enemy_pos[0], enemy_pos[1])
            return range >= d

        def cond_is_surrounded(agent):
            vizinhos = agent.cell.neighborhood.cells 
            for cell in vizinhos:
                if len(cell.agents) != 0:
                    if cell.agents[0].type != 'CHARACTER':
                        return True
            return False

        def cond_friend_attacking(agent):
            vizinhos = agent.cell.get_neighborhood(
                agent.beliefs['displacement']).cells 
            for cell in vizinhos:
                if len(cell.agents) != 0:
                    if cell.agents[0].type == 'CHARACTER' and cell.agents[0].beliefs['em_batalha']:
                        return True
            return False

        # 2. Construir a árvore
        raiz = self._build_tree(
            cond_has_target, 
            cond_enable_atk_enemy,
            cond_friend_attacking,
            cond_is_surrounded
        )
        self.decision_tree = DecisionTree(root=raiz)

    def _build_tree(
            self, 
            cond_has_target,  
            cond_enable_atk_enemy, 
            cond_friend_attacking,  
            cond_is_surrounded):
        """
        Constrói a árvore de decisão...
        """
        # --- PASSO A: Definir todas as FOLHAS (Ações) ---
        acao_atacar = IntentionNode("ATACAR INIMIGO")
        acao_aproximar = IntentionNode("APROXIMAR-SE")
        acao_def_target = IntentionNode("DEFINIR ALVO")
        acao_def_friend_target = IntentionNode("DEFINIR ALVO DO AMIGO")
        acao_def_other_target = IntentionNode("DEFINIR OUTRO ALVO")
        
        # --- PASSO B: Construir os RAMOS (de baixo para cima) ---
        
        ramo_1_2_2 = DecisionNode(
            condition_func=cond_friend_attacking,
            yes_node=acao_def_friend_target,
            no_node=acao_def_other_target)

        ramo_1_1 = DecisionNode(
            condition_func=cond_enable_atk_enemy,
            yes_node=acao_atacar,   
            no_node=acao_aproximar     
        )

        ramo_1_2 = DecisionNode(
            condition_func=cond_is_surrounded,
            yes_node=acao_def_target,   
            no_node=ramo_1_2_2     
        )
        
        raiz = DecisionNode(
            condition_func=cond_has_target, 
            yes_node=ramo_1_1,     
            no_node=ramo_1_2        
        )
        
        return raiz
    
    def get_intention(self, agent):
        """Interface pública para o agente BDI."""
        return self.decision_tree.decide(agent)
