from kedro.pipeline import Pipeline, node, pipeline

from .nodes import evaluate_model, split_data, train_model, predict_from_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_data,
                inputs=["model_input_table", "params:model_options"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split_data_node",
                tags=["training"],
            ),
            node(
                func=train_model,
                inputs=["X_train", "y_train"],
                outputs="regressor",
                name="train_model_node",
                tags=["training"],
            ),
            node(
                func=evaluate_model,
                inputs=["regressor", "X_test", "y_test"],
                outputs="evaluation_metrics",
                name="evaluate_model_node",
                tags=["training"],
            ),
            node(
                func=predict_from_model,
                inputs=[
                    "specific_regressor", 
                    "model_input_table", 
                    "params:model_options.features"],
                outputs="predictions",
                name="predict_node",
                tags=["inference"],
            )
        ]
    )
