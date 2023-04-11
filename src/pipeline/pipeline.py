import numpy as np
import optuna
from darts import TimeSeries
from darts.models.forecasting.forecasting_model import LocalForecastingModel
from optuna import Trial
from optuna.visualization import plot_optimization_history, plot_param_importances

from src.data.dataset import Dataset
from src.pipeline.experiment import Experiment, BayesOptHyperParameter


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

        return {"train": train, "valid": valid, "test": test}

    def run(self):
        print("Fetching Data ...")
        series = self.get_processed_data()
        self.data = self.split_dataset(series)

        print("Beginning Optimization")
        if self.is_bayes_opt():
            self._hparam_search()
        else:
            obj = self._objective()
            print(f"value: {obj}")

    def is_bayes_opt(self) -> bool:
        parameter_types = map(type, self.params.hyper_parameters)
        return BayesOptHyperParameter in parameter_types

    def _hparam_search(self):
        def print_callback(study, trial):
            print(f"Current value: {trial.value}, Current params: {trial.params}")
            print(f"Best value: {study.best_value}, Best params: {study.best_trial.params}")

        study = optuna.create_study(direction="minimize")
        study.optimize(self._objective, timeout=self.params.optuna_timeout, callbacks=[print_callback])

        print(f"Best value: {study.best_value}, Best params: {study.best_trial.params}")
        plot_optimization_history(study)
        plot_param_importances(study)

    def _objective(self, trial: Trial = None):

        # get parameters from experiment definition
        trial_hparams = dict()
        for hparam in self.params.hyper_parameters:
            if type(hparam) == BayesOptHyperParameter:
                # call trial.suggest_method()
                value = getattr(trial, hparam.optuna_suggest_method)(name= hparam.name, **hparam.value)
            else:
                value = hparam.value
            trial_hparams[hparam.name] = value

        # define and fit model
        model = self.params.model(**trial_hparams)

        valid_error = model.backtest(
            series=self.data['train'].append(self.data['valid']),
            start=len(self.data['train']),
            train_length=self.params.n_train_samples,
            stride=len(self.data['valid']) // self.params.n_backtest,
            metric=self.params.metric,
            retrain=isinstance(model, LocalForecastingModel),
            verbose=True
        )

        return valid_error if valid_error != np.nan else float("inf")
