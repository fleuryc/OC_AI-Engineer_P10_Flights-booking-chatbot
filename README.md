# Fly Me : flights booking chatbot

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

Goal : use **Azure Cognitive Services (LUIS)**, **Azure Web App** and **Azure Application Insights**, to build a flights booking chatbot, integrate it in a web application, and monitor its quality.

You can see the results here :

-   [Presentation](https://fleuryc.github.io/OC_AI-Engineer_P10_Flights-booking-chatbot/index.html "Presentation")
-   [Main notebook](https://fleuryc.github.io/OC_AI-Engineer_P10_Flights-booking-chatbot/main.html "Main notebook")
-   [Datataset profile report](https://fleuryc.github.io/OC_AI-Engineer_P10_Flights-booking-chatbot/profile_report.html "Datataset profile report")

This is the project architecture in production :

![center-img h:450px](docs/img/architecture.drawio.png "Current MVP architecture")

## Goals

-   [x] Integrate model output into a finished product :
    -   [Azure Language Understanding - LUIS](https://www.luis.ai/applications "Azure Language Understanding - LUIS") : train and setup a dedicated language understanding model
    -   [Azure App Service](https://portal.azure.com/#@clementfleurypm.onmicrosoft.com/resource/subscriptions/da2e4791-6dd1-422b-848a-a961cef6ab89/resourceGroups/OC_P10_Bot/providers/Microsoft.Web/sites/ocp10-bot-webapp/appServices "Azure App Service") : deploy an interactive API
    -   [Azure Bot - Test in Web Chat](https://portal.azure.com/#@clementfleurypm.onmicrosoft.com/resource/subscriptions/da2e4791-6dd1-422b-848a-a961cef6ab89/resourceGroups/OC_P10_Bot/providers/Microsoft.BotService/botServices/fly_me/test "Azure Bot - Test in Web Chat") : test the bot in a web chat
-   [x] Integrate an AI processing chain into an IT tool using a code version management tool :
    -   [GitHub repository](https://github.com/fleuryc/OC_AI-Engineer_P10_Flights-booking-chatbot "GitHub repository") : manage the code
    -   [Automated tests](https://github.com/fleuryc/OC_AI-Engineer_P10_Flights-booking-chatbot/actions/workflows/python-app.yml?query=branch%3Amain "Automated tests") : test the bot
-   [x] Control the performance of the model in production
    -   [Azure Application Insights](https://portal.azure.com/#@clementfleurypm.onmicrosoft.com/resource/subscriptions/da2e4791-6dd1-422b-848a-a961cef6ab89/resourceGroups/OC_P10_Bot/providers/microsoft.insights/components/ocp10-appinsights/overview "Azure Application Insights") : monitor the quality of the bot

---

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

No known issues...
