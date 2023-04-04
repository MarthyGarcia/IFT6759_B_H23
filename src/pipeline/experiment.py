from dataclasses import dataclass, field
from typing import Type

from darts.dataprocessing import Pipeline
from darts.models.forecasting.forecasting_model import ForecastingModel

@dataclass
class HyperParameter:
    """
    Stores hyper parameter values
    """
    name: str
    value: str | int | float

@dataclass
class BayesOptHyperParameter(HyperParameter):
    optuna_suggest_method: str
    value: dict[str, str | int | float]

    def __post__init(self):
        if self.optuna_suggest_method and not self.optuna_suggest_method.startswith('suggest_'):
            raise ValueError(
                f'{self.optuna_suggest_method} invalid, optuna.Trial'
                + 'requires specific methods, see documentation'
            )


@dataclass(frozen=True)
class Experiment:
    """
    Immutable dataclass to store the parameters of an experiment
    """

    dataset: str
    preprocessing: Pipeline
    model: Type[ForecastingModel]
    metric: callable
    hyper_parameters: list[HyperParameter | BayesOptHyperParameter]
    horizon: int
    optuna_timeout: int
    n_train_samples: int
    n_backtest: int
