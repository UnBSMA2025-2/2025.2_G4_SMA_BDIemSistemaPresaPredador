from Beliefs.beliefs_tree import (
    DecisionTree, 
    DecisionNode, 
    IntentionNode
    )
from utils.get_distance import get_distance

class BattlePlanLogic:
    """
    Esta classe encapsula a lógica de decisão para um agente
    em situações de combate.
    """
    
    def __init__(self):
        # 1. Funções de Condição (Consultas às Crenças)
        #    Estas funções leem o dicionário 'context' (crenças)
        
        def cond_in_battle(agent):
            """Condição 1: em_batalha == true ?"""
            return agent.beliefs['em_batalha']
        
        def cond_enable_atk_enemy(agent):
            # aqui vamos verificar a classe dele e, se 
            # ele não precisar estar lado a lado para atacar,
            # vamos comparar a distância entre ele e o alvo e seu 
            # range de ataque.
            # Retorno: True (se for possível atacar o inimigo) ou 
            # False (se não for possível atacar o inimigo)
            pass

        def cond_is_surrounded(agent):
            # Deve verificar as células vizinhas para ver
            # se existem inimigos ao redor
            vizinhos = agent.cell.neighborhood.cells 
            for cell in vizinhos:
                if len(cell.agents) != 0:
                    if cell.agents[0].type != 'CHARACTER':
                        return True
            return False

        def cond_friend_attacking(agent):
            # deve verificar se algum amigo próximo 
            # tem um alvo
            vizinhos = agent.cell.get_neighborhood(
                agent.beliefs['displacement']).cells 
            for cell in vizinhos:
                if len(cell.agents) != 0:
                    if cell.agents[0].type == 'CHARACTER' and cell.agents[0].beliefs['em_batalha']:
                        print(cell)
                        print(cell.agents[0].type == 'CHARACTER' and cell.agents[0].beliefs['em_batalha'])
                        return True
            return False

        # 2. Construir a árvore e armazenar o "motor"
        raiz = self._build_tree(
            cond_in_battle,
            cond_enable_atk_enemy,
            cond_is_surrounded,
            cond_friend_attacking
        )
        self.decision_tree = DecisionTree(root=raiz)

    def _build_tree(
            self, 
            cond_in_battle, 
            cond_enable_atk_enemy, 
            cond_friend_attacking, 
            cond_is_surrounded):
        """
        Constrói a árvore de decisão de "baixo para cima",
        baseado no rascunho.
        """
        
        # --- PASSO A: Definir todas as FOLHAS (Ações) ---
        acao_atacar = IntentionNode("ATACAR INIMIGO")
        acao_aproximar = IntentionNode("APROXIMAR-SE")
        acao_def_target = IntentionNode("DEFINIR ALVO")
        acao_def_friend_target = IntentionNode("DEFINIR ALVO DO AMIGO")
        acao_def_other_target = IntentionNode("DEFINIR OUTRO ALVO")
        
        # --- PASSO B: Construir os RAMOS (de baixo para cima) ---
        
        # O que fazer se (em_batalha=S) e (alvo_hp_baixo=N)
        ramo_1_1 = DecisionNode(
            condition_func=cond_enable_atk_enemy,
            yes_node=acao_atacar,   
            no_node=acao_aproximar     
        )

        ramo_1_2_2 = DecisionNode(
            condition_func=cond_friend_attacking,
            yes_node=acao_def_friend_target,
            no_node=acao_def_other_target)

        ramo_1_2 = DecisionNode(
            condition_func=cond_is_surrounded,
            yes_node=acao_def_target,   
            no_node=ramo_1_2_2     
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