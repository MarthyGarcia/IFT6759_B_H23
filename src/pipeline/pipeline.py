import numpy as np
import optuna
from darts import TimeSeries
from darts.models.forecasting.forecasting_model import LocalForecastingModel
from optuna import Trial
from optuna.visualization import plot_optimization_history, plot_param_importances

from src.data.dataset import Dataset
from src.pipeline.experiment import Experiment


class ExperimentPipeline:

    def __init__(self, params: Experiment):
        self.params = params
        self.data = None

    def get_raw_data(self) -> TimeSeries:
        return Dataset.get(self.params.dataset)

    def get_processed_data(self) -> TimeSeries:
        raw_data = self.get_raw_data()
        processed_data = self.params.preprocessing.fit_transform(raw_data)
        return processed_data

    def split_dataset(self, series: TimeSeries) -> dict[str, TimeSeries]:
        train, test = series.split_before(0.80)
        train, valid = train.split_before(0.75)

        return {
            'train': train,
            'valid': valid,
            'test': test
        }

    def run(self):
        print('Fetching Data ...')
        series = self.get_processed_data()
        self.data = data = self.split_dataset(series)

        # TODO hparam search (bayes opt)
        # TODO instantiate model with params

        print('Fitting Model ...')
        model = self.params.model()  # TODO params
        model.fit(data['train'])

        retrain = True if isinstance(model, LocalForecastingModel) else False

        print('Computing Valid Error ...')
        valid_error = model.backtest(
            data['valid'],
            stride=self.params.stride,
            metric=self.params.metrics,
            forecast_horizon=self.params.horizon,
            retrain=retrain,
            verbose=True
        )

        print('Computing Test Error ...')
        test_error = model.backtest(
            data['test'],
            stride=self.params.stride,
            metric=self.params.metrics,
            forecast_horizon=self.params.horizon,
            retrain=retrain,
            verbose=True
        )

        print('Done!')

        # TODO return all metrics

    def hparam_search(self):
        def print_callback(study, trial):
            print(f"Current value: {trial.value}, Current params: {trial.params}")
            print(f"Best value: {study.best_value}, Best params: {study.best_trial.params}")

        study = optuna.create_study(direction="minimize")
        study.optimize(self.objective, timeout=7200, callbacks=[print_callback])

        print(f"Best value: {study.best_value}, Best params: {study.best_trial.params}")
        plot_optimization_history(study)
        # plot_contour(study, params=["lr", "num_filters"])
        plot_param_importances(study)

    def objective(self, trial: Trial):
        # Other hyperparameters
        # kernel_size = trial.suggest_int("kernel_size", 5, 25)
        # num_filters = trial.suggest_int("num_filters", 5, 25)
        # weight_norm = trial.suggest_categorical("weight_norm", [False, True])
        # dilation_base = trial.suggest_int("dilation_base", 2, 4)
        # dropout = trial.suggest_float("dropout", 0.0, 0.4)
        # lr = trial.suggest_float("lr", 5e-5, 1e-3, log=True)
        # include_dayofweek = trial.suggest_categorical("dayofweek", [False, True])

        model = self.params.model()  # TODO params suggestion
        model.fit(self.data['train'])

        retrain = True if isinstance(model, LocalForecastingModel) else False
        valid_error = model.backtest(
            self.data['valid'],
            stride=self.params.stride,
            metric=self.params.metrics,
            forecast_horizon=self.params.horizon,
            retrain=retrain,
            verbose=True
        )

        # TODO dynamically setup
        kernel_size = trial.suggest_int("kernel_size", 5, 25)

        return valid_error if valid_error != np.nan else float("inf")



