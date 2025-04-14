# Caminho fixo para ativação do ambiente virtual (Windows-style)
ACTIVATE = .venv/Scripts/activate

.PHONY: activate
activate:
	@$(ACTIVATE) && echo "Virtual environment activated!"

.PHONY: run
run:
	@$(ACTIVATE) && kedro run

.PHONY: train
train:
	@$(ACTIVATE) && kedro run --pipeline=training

.PHONY: inference
inference:
	@$(ACTIVATE) && kedro run --pipeline=inference

.PHONY: report
report:
	@$(ACTIVATE) && kedro run --pipeline=reporting

.PHONY: clean
clean:
	@rmdir /S /Q data/05_model_input 2>nul || echo "model_input not found"
	@rmdir /S /Q data/07_model_output 2>nul || echo "model_output not found"
	@rmdir /S /Q data/08_reporting 2>nul || echo "reporting not found"
	@echo "Cleaned intermediate and output data folders."

.PHONY: install
install:
	@$(ACTIVATE) && pip install -r src/requirements.txt

.PHONY: mlflow
mlflow:
	kedro mlflow ui
