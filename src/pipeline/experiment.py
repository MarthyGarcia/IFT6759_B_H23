from dataclasses import dataclass
from typing import Type

from darts.dataprocessing import Pipeline
from darts.models.forecasting.forecasting_model import ForecastingModel


@dataclass(frozen=True)
class Experiment:
    """
    Immutable dataclass to store the parameters of an experiment
    """
    dataset: str
    preprocessing = Pipeline([])
    model: Type[ForecastingModel]
    metrics: list[callable]
    hyper_parameters: dict[str, list]
    horizon: int
    stride = 1
    seed = 42
