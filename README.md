# Flights booking chatbot

[![Python application](https://github.com/fleuryc/OC_AI-Engineer_P10_Flights-booking-chatbot/actions/workflows/python-app.yml/badge.svg)](https://github.com/fleuryc/OC_AI-Engineer_P10_Flights-booking-chatbot/actions/workflows/python-app.yml)
[![CodeQL](https://github.com/fleuryc/OC_AI-Engineer_P10_Flights-booking-chatbot/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/fleuryc/OC_AI-Engineer_P10_Flights-booking-chatbot/actions/workflows/codeql-analysis.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/06480b57560846a293bed6d5d4f473e1)](https://www.codacy.com/gh/fleuryc/OC_AI-Engineer_P10_Flights-booking-chatbot/dashboard)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/06480b57560846a293bed6d5d4f473e1)](https://www.codacy.com/gh/fleuryc/OC_AI-Engineer_P10_Flights-booking-chatbot/dashboard)

-   [Installation](#installation)
    -   [Prerequisites](#prerequisites)
    -   [Virtual environment](#virtual-environment)
    -   [Dependencies](#dependencies)
    -   [Environment variables](#environment-variables)
-   [Usage](#usage)
    -   [Download data](#download-data)
    -   [EDA (Exploratory Data Analysis)](#eda-exploratory-data-analysis)
    -   [Create a LUIS app in the LUIS portal](#create-a-luis-app-in-the-luis-portal)
    -   [Train LUIS Model](#train-luis-model)
    -   [Test and debug with the Emulator](#test-and-debug-with-the-emulator)
    -   [Tutorial: Provision a bot in Azure](#tutorial-provision-a-bot-in-azure)
    -   [Deploy Bot to Azure Web App](#deploy-bot-to-azure-web-app)
-   [Quality Assurance](#quality-assurance)
-   [Troubleshooting](#troubleshooting)

---

Repository of OpenClassrooms' AI Engineer path, project #10 .

Goal : use Azure Cognitive Services (LUIS), Azure Web App and Azure Application Insights, to build a flights booking chatbot, integrate it in a web application, and monitor its quality.

You can see the results here :

-   Presentation
-   Notebook : HTML page with interactive plots

## Installation

### Prerequisites

-   [Python 3.9](https://www.python.org/downloads/)
-   [Azure Cognitive Services - LUIS](https://www.microsoft.com/cognitive-services/en-us/luis/)

### Virtual environment

```bash
# python -m venv env
# > or just :
make venv
source env/bin/activate
```

### Dependencies

```bash
# pip install -r notebooks/requirements.txt -r bot/requirements.txt
# > or :
# pip install -r requirements.txt
# > or just :
make install
```

### Environment variables

Set environment variable values in (copy or rename `.env.example`) :

-   [.env](.env)
-   [bot/.env](bot/.env)

## Usage

### Download data

Download, and extract the Language Understanding Model (LUIS) training files from [Frames Dataset
](https://www.microsoft.com/en-us/research/project/frames-dataset/download/ "Frames Dataset") :

```bash
make dataset
```

### EDA (Exploratory Data Analysis)

The [`main` notebook](notebooks/main.ipynb) presents the result of the EDA (exploratory data analysis) :

```bash
jupyter-lab notebooks/main.ipynb
```

### Create a LUIS app in the LUIS portal

Follow the official documentation : [Create a LUIS app in the LUIS portal](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-howto-v4-luis?view=azure-bot-service-4.0&tabs=python#create-a-luis-app-in-the-luis-portal= "Create a LUIS app in the LUIS portal")

### Train LUIS Model

The [`luis` notebook](notebooks/luis.ipynb) formats the data, runs the LUIS training and tests the model :

```bash
jupyter-lab notebooks/luis.ipynb
```

### Test and debug with the Emulator

Run the bot locally :

```bash
make bot-start
```

Follow the official documentation : [Test and debug with the Emulator](https://docs.microsoft.com/en-us/azure/bot-service/bot-service-debug-emulator?view=azure-bot-service-4.0&tabs=python "Test and debug with the Emulator")

### Tutorial: Provision a bot in Azure

Follow the official documentation : [Tutorial: Provision a bot in Azure](https://docs.microsoft.com/en-us/azure/bot-service/tutorial-provision-a-bot?view=azure-bot-service-4.0&tabs=userassigned%2Cnewgroup "Tutorial: Provision a bot in Azure")

### Deploy Bot to Azure Web App

Build and deploy the bot to Azure Web App integrating the Bot Service, LUIS and Application Insights :

```bash
make bot-deploy
```

## Quality Assurance

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

This will run tests on the bot [`tests/test_bot.py`](tests/test_bot.py) :

-   [x] test the LUIS service integration
-   [x] test a dialog where the bot gathers the flight informations from the user
-   [x] test a dialog where the user gives all the flight informations at once

## Troubleshooting

-   Fix Plotly issues with JupyterLab

cf. [Plotly troubleshooting](https://plotly.com/python/troubleshooting/#jupyterlab-problems)

```bash
jupyter labextension install jupyterlab-plotly
```

-   If using Jupyter Notebook instead of JupyterLab, uncomment the following lines in the notebook

```python
import plotly.io as pio
pio.renderers.default='notebook'
```
