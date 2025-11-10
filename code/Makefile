VENV_DIR = .venv
PYTHON = python3.12
SOLARA = solara run 

.PHONY: setup run clean help

help:
	@echo "Comandos disponíveis:"
	@echo "  make setup   -> (Requer Python 3.12) Cria o ambiente virtual e instala as dependências."
	@echo "  make run     -> Executa a simulação MESA."
	@echo "  make clean   -> Remove o ambiente virtual e ficheiros temporários."

install: venv
	$(VENV_DIR)/bin/pip install -r requirements.txt

setup:
	@echo "-> Verificando se o $(PYTHON) (Python 3.12) está instalado..."
	@$(PYTHON) -c "import sys; assert sys.version_info >= (3, 12), 'ERRO: Este projeto requer Python 3.12 ou superior. Encontrado: %s' % (sys.version,)"
	@echo "-> Versão do Python OK."

	@echo "-> Verificando/Criando o ambiente virtual em '$(VENV_DIR)'..."
	@test -d $(VENV_DIR) || $(PYTHON) -m venv $(VENV_DIR)
	
	@echo "-> Ativando ambiente e instalando dependências de 'requirements.txt'..."
	. $(VENV_DIR)/bin/activate; pip install -r requirements.txt
	
	@echo "-> Ambiente configurado com sucesso"
	@echo "-> Para executar a simulação, use: make run"

runExample:
	@echo "-> Executando o servidor do exemplo de simulação MESA..."
	. $(VENV_DIR)/bin/activate; $(PYTHON) src/RunExampleModel.py

run:
	@echo "-> Executando o servidor da simulação do mundo RPG..."
	. $(VENV_DIR)/bin/activate; $(SOLARA) src/main.py

test:
	@echo "-> Executando a switch de testes..."
	. $(VENV_DIR)/bin/activate; pytest

clean:
	@echo "-> Removendo ambiente virtual '$(VENV_DIR)'..."
	rm -rf $(VENV_DIR)
	@echo "-> Limpeza concluída."