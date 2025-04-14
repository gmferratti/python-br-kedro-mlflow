import logging

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import max_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


def split_data(data: pd.DataFrame, parameters: dict) -> tuple:
    """Splits data into features and targets training and test sets.

    Args:
        data: Data containing features and target.
        parameters: Parameters defined in parameters/data_science.yml.
    Returns:
        Split data.
    """
    X = data[parameters["features"]]
    y = data["price"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=parameters["test_size"], random_state=parameters["random_state"]
    )
    return X_train, X_test, y_train, y_test


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> LinearRegression:
    """Trains the linear regression model.

    Args:
        X_train: Training data of independent features.
        y_train: Training data for price.

    Returns:
        Trained model.
    """
    specific_regressor = LinearRegression()
    specific_regressor.fit(X_train, y_train)
    return specific_regressor


def evaluate_model(
    specific_regressor: LinearRegression, X_test: pd.DataFrame, y_test: pd.Series
) -> dict[str, float]:
    """Calculates and logs the coefficient of determination.

    Args:
        specific_regressor: Trained model.
        X_test: Testing data of independent features.
        y_test: Testing data for price.
    """
    y_pred = specific_regressor.predict(X_test)
    score = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    me = max_error(y_test, y_pred)
    logger = logging.getLogger(__name__)
    logger.info("Model has a coefficient R^2 of %.3f on test data.", score)
    return {
        "r2_score": {"value": score, "step": 0},
        "mae": {"value": mae, "step": 0},
        "max_error": {"value": me, "step": 0},
    }

def predict_from_model(
    specific_regressor: LinearRegression, 
    model_input_table: pd.DataFrame,
    expected_features: list[str]
) -> pd.DataFrame:
    """
    Generates predictions using a trained model.

    Args:
        specific_regressor: Trained model with a `predict` method.
        model_input_table: Preprocessed input data.
        expected_features: List of features used during training.

    Returns:
        DataFrame containing model predictions.
    """
    data = model_input_table[expected_features]
    preds = specific_regressor.predict(data)
    return pd.DataFrame(preds, columns=["prediction"])