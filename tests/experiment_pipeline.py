import os
import unittest

from darts.metrics import mape, mase, mse
from darts.models import NaiveMean

from src.pipeline.experiment import Experiment
from src.pipeline.pipeline import ExperimentPipeline


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir('..')

    def test_runs(self):
        params = Experiment(
            dataset='traffic',
            model=NaiveMean,
            metrics=[mape, mse],
            hyper_parameters=dict(),  # TODO
            horizon=24,
        )

        pipeline = ExperimentPipeline(params)

        pipeline.run()



if __name__ == '__main__':
    unittest.main()
