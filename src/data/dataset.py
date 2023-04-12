from darts import TimeSeries


class Dataset:
    path = "data/raw/{}/{}.{}"
    
    supported_datasets = []
    
    baseline_datasets = ["electricity", "exchange_rate", "traffic"]
    
    # these datasets have 7 components: open high low close volume trade_count vwap
    crypto_datasets = ["BTC", "ETH"]
    stocks_datasets = ["AAPL", "MSFT", "TSLA", 
          "HD", "WMT", 
          "JPM", "BAC", "MS", "TD",
          "GME", "AMC"
    ]
    
    supported_datasets.extend(baseline_datasets)
    supported_datasets.extend(crypto_datasets)
    supported_datasets.extend(stocks_datasets)

    def __int__(self):
        raise NotImplementedError

    @staticmethod
    def get(dataset: str) -> TimeSeries:
        if dataset not in Dataset.supported_datasets:
            raise ValueError(f"{dataset} not in {Dataset.supported_datasets}")
        
        if dataset in Dataset.baseline_datasets:
            path = Dataset.path.format(dataset, dataset, "txt")
        else:
            path = Dataset.path.format("crypto", dataset, "csv")
            
        series = TimeSeries.from_csv(path, header=None)
        series += 1e-9
        return series.univariate_component(0)  # TODO validate
