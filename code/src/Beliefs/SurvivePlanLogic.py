from Beliefs.beliefs_tree import (
    DecisionTree, 
    DecisionNode, 
    IntentionNode
    )

class SurvivePlanLogic:
    """
    Esta classe encapsula a lógica de decisão para um agente
    em situações de sobrevivência.
    """
    
    def __init__(self):
        # 1. Funções de Condição (Consultas às Crenças)
        #    Estas funções leem o dicionário 'context' (crenças)
        
        def cond_em_batalha(context):
            """Condição 1: em_batalha == true ?"""
            return context['em_batalha']
        
        def cond_alvo_hp_baixo(context):
            """Condição 1.1: agente_alvo.hp < 10% ?"""
            # NOTA: O 'agente_alvo' deve ser um objeto com um atributo 'hp'
            # Assumindo que '10%' significa '< 10' pontos de HP.
            if context['hp_agente_alvo'] is None:
                return False # Não pode ter HP baixo se não há alvo
            return context['hp_agente_alvo'] < 10
        
        def cond_tem_curas(context):
            return context['curas'] > 0

        # 2. Construir a árvore e armazenar o "motor"
        raiz = self._build_tree(
            cond_em_batalha,
            cond_alvo_hp_baixo,
            cond_tem_curas
        )
        self.decision_tree = DecisionTree(root=raiz)

    def _build_tree(self, cond_em_batalha, cond_alvo_hp_baixo, cond_tem_curas):
        """
        Constrói a árvore de decisão de "baixo para cima",
        baseado no rascunho.
        """
        
        # --- PASSO A: Definir todas as FOLHAS (Ações) ---
        acao_atacar = IntentionNode("ATACAR INIMIGO")
        acao_curar = IntentionNode("CURAR")
        acao_fugir = IntentionNode("FUGIR")
        
        # --- PASSO B: Construir os RAMOS (de baixo para cima) ---
        
        # Ramo 1.1.2: O que fazer se (em_batalha=S) e (alvo_hp_baixo=N)
        ramo_1_1_2 = DecisionNode(
            condition_func=cond_tem_curas,
            yes_node=acao_curar,   # C1.1.2.1
            no_node=acao_fugir     # C1.1.2.2
        )

        # Ramo 1.2: O que fazer se (em_batalha=N)
        # (Corrigindo a duplicata C1.2 e C1.2.1 do seu rascunho)
        ramo_1_2 = DecisionNode(
            condition_func=cond_tem_curas,
            yes_node=acao_curar,   # C1.2.1.1
            no_node=acao_fugir     # C1.2.1.2
        )
        
        # Ramo 1.1: O que fazer se (em_batalha=S)
        ramo_1_1 = DecisionNode(
            condition_func=cond_alvo_hp_baixo,
            yes_node=acao_atacar,   # C1.1.1
            no_node=ramo_1_1_2      # Leva ao próximo ramo
        )
        
        # --- PASSO C: Construir a RAIZ ---
        raiz = DecisionNode(
            condition_func=cond_em_batalha,
            yes_node=ramo_1_1,      # Caminho C1.1
            no_node=ramo_1_2        # Caminho C1.2
        )
        
        return raiz

    def get_intention(self, context):
        """Interface pública para o agente BDI."""
        return self.decision_tree.decide(context)