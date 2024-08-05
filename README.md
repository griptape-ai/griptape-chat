# Griptape Chat Demo 

## Description
This repository contains Python code using the [griptape](https://github.com/griptape-ai) framework that allows you to interact with a Griptape Structure through the [Gradio ChatInterface](https://www.gradio.app/docs/gradio/chatinterface). 

The demo uses [Gradio](https://www.gradio.app/) for the frontend and [Griptape](https://github.com/griptape-ai/griptape) for the backend.

## Get the code
```shell
git pull git@github.com:griptape-ai/griptape-chat.git
cd griptape-chat
```

### OpenAI API Key
We'll need to obtain our OpenAI API key. Follow the steps below to do so:

1. Head to [OpenAi's official website](https://platform.openai.com/) and either create or login to your account.
Once you are logged in, click on the "Personal" text on the top right of your browser and then click on 
"View API keys" from the context menu that appears.

1. Click on "+ Create new secret key" and give it a name.
1. Copy the key and paste it in the .env file in the root directory of this project. Replacing "your key here" 

## Setting up the runtime environment
Copy the .env.example into a .env in the root of this project directory and populate your OPENAI_API_KEY:
 ```shell
 OPENAI_API_KEY=your key here
 ```

*optional: if you want to run this on a port other than the default gradio port of 7860 you  can add 
GRADIO_PORT=<your port here> to the .env file as well*

### Cloud Based Conversation Memory
Follow the link and the instructions in the README to set up the [Griptape Structure Chatbot](https://github.com/griptape-ai/griptape-structure-chatbot) structure and CDK. 
This will create your lambda endpoint and [Griptape Structure ID](https://cloud.griptape.ai/structures).
```shell
GT_STRUCTURE_ID=<your-structure-id>
LAMBDA_ENPOINT=<your-lambda-endpoint>
```

## Running the Demo

If you would like to run the demo locally, then COMMENT OUT these variables in your .env. 
```shell
    GT_STRUCTURE_ID=
    GT_CLOUD_BASE_URL=
    LAMBDA_ENDPOINT=
    GT_CLOUD_API_KEY=
```

If you would like to run the demo in a managed environment, like Skatepark or Griptape Cloud, then define these variables in your .env: 
```shell
GT_STRUCTURE_ID=<YourStructureID> 
GT_CLOUD_BASE_URL=https://cloud.griptape.ai or http://127.0.0.1:5000
LAMBDA_ENDPOINT=<YourLambdaEndpoint>
GT_CLOUD_API_KEY=<YourCloudAPIKey>
```

### via poetry
```shell
poetry install
poetry run python app.py
```

### via docker

```shell
docker-compose up;
```