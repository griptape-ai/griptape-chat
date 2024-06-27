# Griptape Structure Chat Demo

The demo uses [Gradio](https://www.gradio.app/) for the frontend and [Griptape Cloud](https://www.griptape.ai/cloud) for the backend.

## Get the code

```shell
git pull git@github.com:griptape-ai/griptape-chat.git
cd griptape-chat
```

## Setting up the runtime environment

Create file called .env in the root of this project directory and add the following content:

```shell
GT_CLOUD_API_KEY=
GT_CLOUD_STRUCTURE_ID=
```

_optional: if you want to run this on a port other than the default gradio port of 7860 you can add
GRADIO_PORT=<your port here> to the .env file as well_

## Running the Demo

### via poetry

```shell
poetry install
poetry run python app.py
```

### via docker

```shell
docker-compose up;
```
