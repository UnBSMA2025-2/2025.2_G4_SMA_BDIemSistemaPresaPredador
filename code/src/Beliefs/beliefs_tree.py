class IntentionNode:
    """
    Um nó folha que representa uma ação/intenção final.
    """
    def __init__(self, intention):
        self.intention = intention

class DecisionNode:
    """
    Um nó interno (de decisão) que faz uma pergunta.
    Sempre tem dois filhos: um para 'Sim' (True) e um para 'Não' (False).
    """
    def __init__(self, condition_func, yes_node, no_node):
        # 'condition_func' é uma função (ou lambda) que recebe 
        # o 'contexto' e retorna True ou False.
        self.condition_func = condition_func
        
        # 'yes_node' e 'no_node' são os próximos nós (podem ser
        # outro DecisionNode ou um IntentionNode)
        self.yes_node = yes_node
        self.no_node = no_node

class DecisionTree:
    """
    A árvore que gerencia a navegação.
    Começa na raiz e segue até uma folha.
    """
    def __init__(self, root):
        self.root = root  # A raiz deve ser um DecisionNode

    def decide(self, agent):
        """
        Toma uma decisão com base em um 'contexto' (estado atual).
        'context' é um dicionário ou objeto com os dados para as condições.
        """
        current_node = self.root
        
        # Navega na árvore enquanto formos um nó de decisão
        while isinstance(current_node, DecisionNode):
            # A função da condição é chamada com o contexto
            if current_node.condition_func(agent):
                current_node = current_node.yes_node
            else:
                current_node = current_node.no_node
        
        # Quando o loop acabar, 'current_node' é um IntentionNode.
        # Retornamos a intenção armazenada nele.
        return current_node.intention