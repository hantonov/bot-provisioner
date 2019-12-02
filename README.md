# Provisioning BOT

Eventually it will be a bot to provision servers.

## to test locally

start the flask application

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pip-tools
pip-compile
pip-sync requirements.txt
python app.py
```

connect the bot emulator to <http://localhost:3978/api/messages>

## Setting up in Azure

To view the list of supported environments in azire App service `az webapp list-runtimes --linux`. Currently using `"PYTHON|3.7"`

## Access diagnostics logs

```bash
az webapp log config --name <app-name> --resource-group myResourceGroup --docker-container-logging filesystem
az webapp log tail --name <app-name> --resource-group myResourceGroup
```

more configuration and diagnostics information is [here](https://docs.microsoft.com/en-us/azure/app-service/containers/how-to-configure-python)
