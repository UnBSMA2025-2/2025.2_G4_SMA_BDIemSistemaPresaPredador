# Simulador de RPG com Agentes BDI

**Disciplina**: FGA0053 - Sistemas Multiagentes <br>
**Nro do Grupo (de acordo com a Planilha de Divisão dos Grupos)**: 04<br>
**Frente de Pesquisa**: Modelo BDI aplicado a simulações de mundo de RPG (Role-Playing Game)<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 21/1039662  |  Pedro Henrique da Silva Melo |
| 22/2025914  |  Marllon Fausto Cardoso |
| 20/2063300  |  João Pedro Rodrigues Morbeck |
| 19/0117508  |  Thiago Cerqueira Borges |

## Sobre 
Descreva o seu projeto em linhas gerais. 
Use referências, links, que permitam conhecer um pouco mais sobre o projeto.
Capriche nessa seção, pois ela é a primeira a ser lida pelos interessados no projeto.

O nosso projeto simula um mundo de RPG (Role-Playing Game) simples utilizando a arquitetura de Sistemas Multiagentes (MAS) e o framework MESA em Python. O objetivo principal não é criar um jogo, mas sim modelar o comportamento emergente de agentes inteligentes num ambiente de mundo aberto.

O núcleo do nosso sistema é a implementação do modelo de agência **BDI (Belief-Desire-Intention)**:

## Modelo BDI

### Agentes
O mundo é populado por Character_Agent (os heróis, controlados pelo BDI), Mob_Agent e Enemy_Agent (os inimigos que atacam os heróis).

### Crenças (Beliefs) 
Os agentes têm uma percepção limitada do mundo. Eles "sabem" informações como o seu nome, HP, se há inimigos próximos, se há itens de cura próximos, e (no caso dos Character_Agent) mantêm uma "memória" de células recentemente visitadas.

### Desejos (Desires) 

O comportamento do agente é guiado por uma hierarquia de desejos. Usamos um arquivo `CharacterDesires.py` que serve como "Maestro" que decide a prioridade do agente a cada passo:

1. **'SURVIVE'** (Sobreviver): Desejo ativado se o HP estiver baixo.

2. **'BATTLE'** (Batalhar): Desejo ativado se o HP estiver OK e houver inimigos próximos.

3. **'EXPLORE'** (Explorar): O desejo padrão se o agente estiver seguro e saudável.

4. **Futuros Desejos/Desires a serem desenvolvidos**: Descrição

### Intenções (Intentions)

Com base no Desejo ativo, o agente consulta uma "Biblioteca de Planos" (plan_library) e seleciona um plano de ação detalhado para executar suas ações e intenções em cada passo da simulação.

### Planos

Estes planos são implementados como Árvores de Decisão que geram ações concretas (Intenções) como ATACAR INIMIGO, APROXIMAR DO ITEM ou EXPLORAR (que usa a nossa lógica de "exploração inteligente" para evitar repetições).

### Objetivos
A simulação permite-nos observar como estes agentes BDI autônomos gerenciam as suas prioridades e interagem com o o mundo, com outros agentes, com os itens e entre si.

## Vídeo
[Clique aqui!](https://www.youtube.com/watch?v=MZNgeq5jD30)

## Screenshots
![Captura de tela de 2025-11-04 08-24-08](https://drive.google.com/file/d/13q0rm-udvfWCABHmJJG0qRPkS_KDEKFS/view?usp=sharing)<br>
![Captura de tela de 2025-11-04 08-27-22](https://drive.google.com/file/d/1G0NofoJ6uaz8TJjUcFYwW2nGaxjn94t6/view?usp=sharing)


## Instalação 
**Linguagens**: Python<br>
**Tecnologias**: MESA<br>
Descreva os pré-requisitos para rodar o seu projeto e os comandos necessários.
Insira um manual ou um script para auxiliar ainda mais.
Gifs animados e outras ilustrações são bem-vindos!

### Pré-requisitos
* Python 3.12 ou acima

### Configuração de ambiente via Makefile (Linux)
Para configurar o ambiente, primeiro entre dentro da pasta code a partir da raiz do projeto:
```
cd code
```
Em seguida, execute, **APENAS UMA VEZ**, o comando abaixo para instalar o ambiente virtual python (venv) junto com as dependências do projeto, como o MESA framework:
```
make setup
```
Para iniciar o ambiente configurado, execute o seguinte comando:
```
make run
```
Se quiser limpar o ambiente, e reiniciar novamente, pode fazer por meio do comando:
```
make clean
```

### Instalação Manual (Windows/macOS/Linux)
Recomendamos a criação de um ficheiro requirements.txt com as seguintes dependências:

    mesa
    solara
    numpy
    pandas
    seaborn
    matplotlib

1. Crie o ambiente virtual:
        
```
python3 -m venv .venv
```

2. Ative o ambiente:
* No Linux/macOS: `source .venev/bin/activate`
* No Windows: `.venv\Scripts\activate`

3. Instale as dependências:

```
pip install -r requirements.txt
```

4. Execute o servidor:
```
solara run src/main.py
```
O servidor estará disponível em http://localhost:8765 (ou na porta que o Solara indicar).

## Uso 

Após executar `make run` ou `solara run src/main.py` e abrir o seu navegador (ex: `http://localhost:8765`):

1.  **Interface Principal:** Você verá a interface do SolaraViz.
    * **À Esquerda (Painel de Controlo):** Aqui pode iniciar (`PLAY`), pausar, avançar passo-a-passo (`STEP`) ou reiniciar (`RESET`) a simulação. Pode também ajustar os `Model Parameters` (como o número de agentes) antes de clicar em `RESET`.
    * **À Direita (Visualização):** O grid que mostra a simulação.
        * **Agentes Pretos:** São os `Character_Agent` (controlados pelo BDI).
        * **Agentes Vermelhos:** São os `Mob_Agent` (inimigos).
        * Células Verdes: são os `healing_item_spot` que representam um item de cura na qual os agentes podem adquirir para aumentar o número de curas disponíveis.

2.  **Observando o Comportamento:**
    * Clique em `PLAY` para deixar a simulação correr ou `STEP` para analisar passo a passo.
    * **Observe o seu Terminal:** O *log* do terminal é a parte mais importante. Ele mostra a "mente" de cada agente BDI.
    * Você verá os agentes `Character_Agent` a executar o seu ciclo BDI e a declarar as suas intenções a cada passo:
        ```log
        INTENÇÃO [4]: EXPLORAR
        PLANO EM ANDAMENTO [4]: EXPLORE
        ```
    * Quando um agente (no seu modo `EXPLORE`) se aproxima de um inimigo, o seu `get_desire` mudará o plano para `BATTLE`.
    * Quando um agente (no seu modo `EXPLORE`) se aproxima de um item, a sua intenção mudará para `APROXIMAR DO ITEM` e depois `ADQUIRIR ITEM`.

## Participações
Apresente, brevemente, como cada membro do grupo contribuiu para o projeto.
|Nome do Membro | Contribuição | Significância da Contribuição para o Projeto (Excelente/Boa/Regular/Ruim/Nula) | Comprobatórios (ex. links para commits)
| -- | -- | -- | -- |
| Pedro Henrique da Silva Melo  |  Programação do modelo BDI para exploração dos agentes, criação das células com itens de cura, pesquisa científica para artigos voltados para sistemas multi-agentes comportamentais | Boa | [Pull Request](https://github.com/UnBSMA2025-2/2025.2_G4_SMA_BDIemSistemaPresaPredador/pull/5)
| 	Marllon Fausto Cardoso  | Idealização e implementação da base lógica dos agentes BDI e sua comunicação: <br>1. Implementação das classes da árvore de decisão (estrutura e nós);<br>2. Implementação da árvore de decisão de Sobrevivência do character_agent;<br>3. Implementação da árvore de decisão de Combate do character_agent e seus métodos de ação;<br>4. Implementação da árvore de decisão de Reação a Ataques do mob_agent e seus métodos de ação;<br> 5. Implementação da interface IBDI_Agent que estabelece o contrato da lógica BDI para todos os agentes do modelo;<br>6. Implementação da lóica de troca de mensagens entre os agentes do modelo;   | Excelente | [Pull Request](https://github.com/UnBSMA2025-2/2025.2_G4_SMA_BDIemSistemaPresaPredador/pull/1)<br>[Pull Request](https://github.com/UnBSMA2025-2/2025.2_G4_SMA_BDIemSistemaPresaPredador/pull/2)<br>[Pull Request](https://github.com/UnBSMA2025-2/2025.2_G4_SMA_BDIemSistemaPresaPredador/pull/3)<br>[Pull Request](https://github.com/UnBSMA2025-2/2025.2_G4_SMA_BDIemSistemaPresaPredador/pull/4/commits)<br>
| João Pedro Rodrigues Morbeck |  Criação dos agentes enemy e animal, criação dos planos lógicos de sobrevivência do enemy e animal | Regular | [Pull Request](https://github.com/UnBSMA2025-2/2025.2_G4_SMA_BDIemSistemaPresaPredador/pull/6)<br>[Pull Request](https://github.com/UnBSMA2025-2/2025.2_G4_SMA_BDIemSistemaPresaPredador/pull/12)<br>
| Thiago Cerqueira Borges  |  Programação dos Fatos da Base de Conhecimento Lógica | Boa | [Pull Request](https://github.com/UnBSMA2025-2/2025.2_G4_SMA_BDIemSistemaPresaPredador/pull/10)<br>[Pull Request](https://github.com/UnBSMA2025-2/2025.2_G4_SMA_BDIemSistemaPresaPredador/pull/11)<br>

## Outros

Aqui estão algumas das nossas perceções e lições aprendidas durante o desenvolvimento do projeto:

* **(i) Percepções:**
    * O MESA é excelente para modelação, mas a sua API de visualização está em transição (o antigo `ModularServer` vs. o novo `SolaraViz`).
    * A abordagem de visualização com `SpaceRenderer(backend="matplotlib")` é funcional para depuração, mas é estática (gera uma nova imagem a cada passo) e não permite a renderização dinâmica.

* **(ii) Contribuições e Fragilidades:**
    * **Contribuições:** Conseguimos implementar um ciclo BDI hierárquico completo. A nossa lógica de "Exploração Inteligente" com memória (`visited_cells` e `exploration_cooldown`) é uma contribuição robusta que impede comportamentos repetitivos e oscilações, forçando o agente a explorar novas áreas.

* **(iii) Trabalhos Futuros:**
    * **Expandir o BDI:** Implementar os diferentes planos de "Procurar Cura" por classe (Guerreiro, Mago, Caçador) que desenhámos na nossa árvore de exploração, mas que ainda não estão implementados.

## Fontes

* **MESA Framework:** A documentação oficial do MESA, usada como referência principal para a API do modelo e do grid.
    * Disponível em: [https://mesa.readthedocs.io/](https://mesa.readthedocs.io/)
* **Solara:** A biblioteca usada pelo MESA 3.x para a visualização web.
    * Disponível em: [https://solara.dev/](https://solara.dev/)
* **Arquitetura BDI (Referência Teórica):**
    * Rao, A. S., & Georgeff, M. P. (1995). BDI agents: from theory to practice. *Proceedings of the first international conference on Multi-agent systems*.
* **Tutorial MESA (Boltzmann Wealth Model):** O tutorial de visualização do MESA que usámos como base para a integração com o `SolaraViz` e `SpaceRenderer`.
    * Disponível na documentação oficial do MESA.
