import os
import unittest

from darts.metrics import mape, mase, mse
from darts.models import NaiveMean, ARIMA

from src.pipeline.experiment import Experiment, HyperParameter, BayesOptHyperParameter
from src.pipeline.pipeline import ExperimentPipeline


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir('..')

    def test_runs_set_hparams(self):
        params = Experiment(
            dataset='traffic',
            model=ARIMA,
            hyper_parameters=list(),
            metric=mse,
        )

        pipeline = ExperimentPipeline(params)
        pipeline.run()

    def test_runs_bayes_search(self):
        params = Experiment(
            dataset='traffic',
            model=ARIMA,
            hyper_parameters=[
                BayesOptHyperParameter(
                    name='p',
                    optuna_suggest_method='suggest_int',
                    value=dict(low=1, high=20),
                ),
                HyperParameter(
                    name='d',
                    value=3
                ),
                BayesOptHyperParameter(
                    name='q',
                    optuna_suggest_method='suggest_int',
                    value=dict(low=1, high=5)
                ),
            ],
            metric=mse,
            optuna_timeout=60,
            horizon=24*7,
            n_backtest=1,
            n_train_samples=100
        )

        pipeline = ExperimentPipeline(params)
        pipeline.run()



if __name__ == '__main__':
    unittest.main()
