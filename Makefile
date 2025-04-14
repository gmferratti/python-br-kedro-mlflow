# Caminho de ativação do ambiente virtual (bash no Windows)
ACTIVATE = source .venv/Scripts/activate

.PHONY: activate
activate:
	@$(ACTIVATE) && echo "✅ Virtual environment activated."

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
	@rm -rf data/05_model_input || echo "⚠️ model_input not found"
	@rm -rf data/07_model_output || echo "⚠️ model_output not found"
	@rm -rf data/08_reporting || echo "⚠️ reporting not found"
	@echo "🧹 Cleaned intermediate and output data folders."

.PHONY: install
install:
	@$(ACTIVATE) && pip install -r src/requirements.txt && echo "📦 Dependencies installed."

.PHONY: mlflow
mlflow:
	@kedro mlflow ui