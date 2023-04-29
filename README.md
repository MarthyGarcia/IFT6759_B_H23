Forecasting Time Series
==============================

This repository is meant for the analysis of time series forecasting state of the art for cryptocurrency applications.

It is made in the context of the course _IFT-6759: Advanced ML project_

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Interface for local datasets
        │   └── ...
        │
        ├── gdrive         <- Scripts to download or generate data
        │   └── ...
        │
        └── pipeline       <- Scripts to train models and then use trained models to make
            │                 predictions as well as hyper parameter search
            └── ...

--------


To Get You Started
--------
This project uses [makefiles](https://opensource.com/article/18/8/what-how-makefile) to automate the common workflows within the pipeline

To get started with this project install [make](https://sp21.datastructur.es/materials/guides/make-install.html), then type `make` in your terminal. This will list available commands

Then type `make create_environment`, `make requirements` and finally `make test_environment` to verify the setup.



---
<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
