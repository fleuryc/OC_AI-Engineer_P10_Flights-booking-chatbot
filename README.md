# Flights booking chatbot

[![Python application](https://github.com/fleuryc/OC_AI-Engineer_P10_Flights-booking-chatbot/actions/workflows/python-app.yml/badge.svg)](https://github.com/fleuryc/OC_AI-Engineer_P10_Flights-booking-chatbot/actions/workflows/python-app.yml)
[![CodeQL](https://github.com/fleuryc/OC_AI-Engineer_P10_Flights-booking-chatbot/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/fleuryc/OC_AI-Engineer_P10_Flights-booking-chatbot/actions/workflows/codeql-analysis.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/06480b57560846a293bed6d5d4f473e1)](https://www.codacy.com/gh/fleuryc/OC_AI-Engineer_P10_Flights-booking-chatbot/dashboard)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/06480b57560846a293bed6d5d4f473e1)](https://www.codacy.com/gh/fleuryc/OC_AI-Engineer_P10_Flights-booking-chatbot/dashboard)

- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Virtual environment](#virtual-environment)
  - [Dependencies](#dependencies)
- [Usage](#usage)
  - [Download data](#download-data)
  - [Run Notebook](#run-notebook)
  - [Quality Assurance](#quality-assurance)
- [Troubleshooting](#troubleshooting)

---

Repository of OpenClassrooms' AI Engineer path, project #10 .

Goal : use Azure Machine Learning, azure Cognitive Services (LUIS) and Azure Web App, to build a flights booking chatbot and integrate it in a web application.

You can see the results here :

- Presentation
- Notebook : HTML page with interactive plots

## Installation

### Prerequisites

- [Python 3.9](https://www.python.org/downloads/)

### Virtual environment

```bash
# python -m venv env
# > or just :
make venv
source env/bin/activate
```

### Dependencies

```bash
# pip install jupyterlab ipykernel ipywidgets widgetsnbextension graphviz python-dotenv requests matplotlib seaborn plotly bokeh dtale lux-api pandas-profiling autoviz great_expectations popmon numpy statsmodels pandas modin[ray] sklearn torch tensorflow
# > or :
# pip install -r requirements.txt
# > or just :
make install
```

### Environment variables

- Set environment variable values in [.env](.env) file (copy or rename [.env.example](.env.example)).

## Usage

### Download data

Download, extract and upload to Azure Cityscape zip files.

```bash
make dataset
```

### Run Notebook

```bash
jupyter-lab notebooks/main.ipynb
```

### Quality Assurance

```bash
# make isort
# make format
# make lint
# make bandit
# make mypy
# make test
# > or just :
make qa
```

## Troubleshooting

- Fix Plotly issues with JupyterLab

cf. [Plotly troubleshooting](https://plotly.com/python/troubleshooting/#jupyterlab-problems)

```bash
jupyter labextension install jupyterlab-plotly
```

- If using Jupyter Notebook instead of JupyterLab, uncomment the following lines in the notebook

```python
import plotly.io as pio
pio.renderers.default='notebook'
```
