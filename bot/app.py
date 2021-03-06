import asyncio
from datetime import datetime

from flask import Flask, request, Response
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    ConversationState,
    MemoryStorage,
    UserState,
)

from botbuilder.schema import Activity
from .bots import DialogBot
from .dialogs import UserProfileDialog
from .adapter_with_error_handler import AdapterWithErrorHandler

# Create the loop and Flask app

loop = asyncio.get_event_loop()
app = Flask(__name__, instance_relative_config=True)

#app.config.from_object("config.DefaultConfig")
app.config.from_envvar('BOT_APPLICATION_SETTINGS')

settings = BotFrameworkAdapterSettings(app.config["APP_ID"], app.config["APP_PASSWORD"])

memory = MemoryStorage()
user_state = UserState(memory)
conversation_state = ConversationState(memory)

adapter = AdapterWithErrorHandler(settings, conversation_state)
dialog = UserProfileDialog(user_state)
bot = DialogBot(conversation_state, user_state, dialog)

@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)
    
    activity = Activity().deserialize(body)
    auth_header = (
        request.headers["Authorization"] if  "Authorization" in request.headers else ""
    )

    try:
        task = loop.create_task(
            adapter.process_activity(activity, auth_header, bot.on_turn)
        )
        loop.run_until_complete(task)
        return Response(status=201)
    except Exception as ex:
        raise ex

@app.route("/test/hello")
def test_hello():
    return("The bot is alive - " + str(datetime.utcnow()))

if __name__ == "__main__":
    try:
        app.run(debug=False, port=app.config["PORT"], host='0.0.0.0') # nosec debug
    except Exception as ex:
        raise ex