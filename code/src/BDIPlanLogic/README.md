---
title: 'Guia: Árvores de Decisão no Projeto BDI'

---

# Guia: Árvores de Decisão no Projeto BDI

Para implementar a representação do modelo BDI (Belief-Desire-Intention), optamos pelo uso de Árvores de Decisão Binárias.

## 1. O Conceito: Árvores como Planos BDI

A arquitetura BDI define que um agente decide o que fazer através de um ciclo de deliberação. Nossas árvores de decisão mapeiam diretamente para este ciclo:

**1. Crenças (Beliefs):** São o estado do mundo que o agente percebe.Neste projeto, é seu dicionário agent.beliefs.

**2. Desejos (Desires):** São os objetivos de alto nível do agente (ex: "Quero sobreviver", "Quero explorar"). Aqui, os módulos "CharacterDesires.py", "EnemyDesires.py" e "AnimalDesires.py" analisa as Crenças e seleciona o Desejo mais urgente (ex: 'SURVIVE' se o HP estiver baixo).

**3. Planos (Plans):** São a "receita" (o como fazer) para alcançar um Desejo.Nesse contexto, esta é a nossa Árvore de Decisão. Cada Desejo é mapeado para uma classe de lógica (ex: SurvivePlanLogic, BattlePlanLogic e outras) que contém uma Árvore de Decisão inteira.

**4. Intenções (Intentions):** São o plano específico que o agente se compromete a executar agora. Se trata do resultado final da árvore (o nó folha). É uma string simples (ex: "ATACAR INIMIGO", "FUGIR") que o agente usará em seu execute_plan.

## 2. A Implementação: Motor vs. Lógica

Para manter o código limpo e escalável, separamos a nossa arquitetura em duas partes:

O "Motor" Genérico (beliefs_tree.py)

Este arquivo contém as três classes genéricas que formam o "motor" de qualquer árvore. Elas apenas possuem a função de navegar pela estrutura de uma árvore.

**1. IntentionNode:** Representa uma folha (uma ação final, como "CURAR").

**2. DecisionNode:** Representa um ramo (uma pergunta/condição, como hp > 50%?). Ele armazena qual nó seguir para "Sim" e qual para "Não".

**3. DecisionTree:** A classe principal que gerencia a árvore. Ela recebe a raiz e possui um único método, decide(agent), que navega pela árvore com base nas crenças do agente e retorna a IntentionNode final.

Para cada Desejo, criamos uma classe de lógica específica (ex: SurvivePlanLogic, BattlePlanLogic, ExplorationPlanLogic). Esta classe encapsula toda a complexidade daquele plano:

* Define as Funções de Condição: São os métodos privados que sabem como "perguntar" às crenças do agente (ex: cond_target_low_hp, cond_is_surrounded).

* Constrói a Árvore: O método build_tree instancia todos os IntentionNode (ações) e os DecisionNode (perguntas) e os "conecta" de baixo para cima, retornando o nó raiz.

* Interface Pública: Possui um único método público, get_intention(agent), que simplesmente chama o self.decision_tree.decide(agent).

## 3. Nossas Árvores Atuais

**1. SurvivePlanLogic:** Focado em sobrevivência individual para o agente Character_Agent. Decide entre atacar, curar, fugir, ou pedir cura a amigos, com base no HP e nos itens de cura.
![image](https://hackmd.io/_uploads/HkVAYSkgbl.png)

**2. BattlePlanLogic:** Lógica de combate tático para o agente Character_Agent. Decide como adquirir um alvo (adjacente, alvo do amigo, ou buscar) quando o agente não tem um.
![image](https://hackmd.io/_uploads/HJErcBJgWx.png)

**3. RetaliateAttackPlanLogic:** Lógica de reação. É ativada quando o agente é atacado, decidindo se deve contra-atacar, aproximar-se ou definir o atacante como alvo.
![image](https://hackmd.io/_uploads/ryzuqHyl-l.png)

**4. ExplorationPlanLogic:** Lógica de "tempo ocioso". Decide entre explorar aleatoriamente, buscar itens de cura no mapa ou atacar inimigos próximos se estiver com HP baixo.
![image](https://hackmd.io/_uploads/rkys9rJeZl.png)

**5. SurviveAnimalPlanLogic:** Lógica de sobrevivência para o agente Animal_Agent. Decide entre explorar, fugir de um agente próximo ou aproximar-se de um agente igual próximo.
![image](https://hackmd.io/_uploads/BkjyoSJgWg.png)

## 4. Como Adicionar um Novo Plano/Árvore

**Crie a Lógica:** Crie um novo arquivo (ex: NewPlanLogic.py) seguindo o modelo de SurvivePlanLogic.

**Defina as Condições:** Implemente as funções de condição (ex: cond_exemplo).

**Construa a Árvore:** Mapeie sua lógica no _build_tree, criando os IntentionNode (ações) e DecisionNode (perguntas).

**No Agente:** adicione as novas ações (intenções) ao execute_plan (ex: case 'NOVA_ACAO': self.nova_acao()). Adicione sua nova classe de lógica à plan_library no __init__ do agente (ex: 'NEW_PLAN': NewPlanLogic()). Adicione a lógica para selecionar este novo desejo.
