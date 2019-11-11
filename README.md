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
