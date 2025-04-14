"""Project pipelines."""
from kedro.pipeline import Pipeline
from typing import Dict

from spaceflights.pipelines.data_processing.pipeline import create_pipeline as create_data_processing_pipeline
from spaceflights.pipelines.data_science.pipeline import create_pipeline as create_data_science_pipeline
from spaceflights.pipelines.reporting.pipeline import create_pipeline as create_reporting_pipeline


def register_pipelines() -> Dict[str, Pipeline]:
    # Pipelines modulares
    data_processing_pipeline = create_data_processing_pipeline()
    data_science_pipeline = create_data_science_pipeline()
    reporting_pipeline = create_reporting_pipeline()

    # Pipeline completo de machine learning (pré-processamento + modelagem)
    full_ml_pipeline = data_processing_pipeline + data_science_pipeline

    # Subconjunto de nós usados exclusivamente para treino do modelo
    training_nodes_pipeline = full_ml_pipeline.only_nodes_with_tags("training")

    # Pipeline de inferência completo: inclui modelo + gráficos + métricas
    full_inference_pipeline = full_ml_pipeline.only_nodes_with_tags("inference") + reporting_pipeline

    # Pipeline padrão (tudo)
    default_pipeline = data_processing_pipeline + data_science_pipeline + reporting_pipeline

    return {
        "training": training_nodes_pipeline,            # usado para MLflow
        "inference": full_inference_pipeline,        # para reuso em produção ou análise
        "reporting": reporting_pipeline,             # somente relatórios
        "__default__": default_pipeline,             # tudo, para facilitar execução completa
    }