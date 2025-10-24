VENV_DIR = .venv
PYTHON = python3

.PHONY: setup run clean help

help:
	@echo "Comandos disponíveis:"
	@echo "  make setup   -> Cria o ambiente virtual e instala todas as dependências."
	@echo "  make run     -> Executa a simulação MESA."
	@echo "  make clean   -> Remove o ambiente virtual e ficheiros temporários."

install: venv
	$(VENV_DIR)/bin/pip install -r requirements.txt

setup:
	@echo "-> Verificando/Criando o ambiente virtual em '$(VENV_DIR)'..."
	@test -d $(VENV_DIR) || $(PYTHON) -m venv $(VENV_DIR)
	
	@echo "-> Ativando ambiente e instalando dependências de 'requirements.txt'..."
	. $(VENV_DIR)/bin/activate; pip install -r requirements.txt
	
	@echo "-> Ambiente configurado com sucesso"
	@echo "-> Para executar a simulação, use: make run"

run:
	@echo "-> Executando o servidor da simulação MESA..."
	. $(VENV_DIR)/bin/activate; $(PYTHON) src/run.py

clean:
	@echo "-> Removendo ambiente virtual '$(VENV_DIR)'..."
	rm -rf $(VENV_DIR)
	@echo "-> Limpeza concluída."