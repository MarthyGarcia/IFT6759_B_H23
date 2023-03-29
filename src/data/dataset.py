from darts import TimeSeries


class Dataset:
    path = 'data/raw/{}/{}.txt'
    supported_datasets = [
        'electricity',
        'exchange_rate',
        'traffic'
    ]

    def __int__(self):
        raise NotImplementedError

    @staticmethod
    def get(dataset: str) -> TimeSeries:
        if dataset not in Dataset.supported_datasets:
            raise ValueError(f'{dataset} not in {Dataset.supported_datasets}')

        path = Dataset.path.format(dataset, dataset)
        series = TimeSeries.from_csv(path, header=None)
        series += 1e-9
        return series.univariate_component(0)  # TODO validate
