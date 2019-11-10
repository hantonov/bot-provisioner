import sys
from datetime import datetime


from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    ConversationState,
    TurnContext,
)
from botbuilder.schema import InputHints, ActivityTypes, Activity

class AdapterWithErrorHandler(BotFrameworkAdapter):
    def __init__(
        self,
        settings: BotFrameworkAdapterSettings,
        conversation_state: ConversationState,
    ):
        super().__init__(settings)
        self._conversation_state = conversation_state

        # Catch-all for errors
        async def on_error(context: TurnContext, error: Exception):
            # TODO: replace with logging (Azure insights)
            print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)

            # Send message to the user
            await context.send_activity("The bot encountered an error or bug.")
            await context.send_activity("To continue to run this bot, please fix the bot source code.")
            if context.activity.channel_id == 'emulator':
                trace_activity = Activity(
                    label="TurnError",
                    name="on_turn_error Trace",
                    timestamp=datetime.utcnow(),
                    type=ActivityTypes.trace,
                    value=f"{error}",
                    value_type="https://www.botframework.com/schemas/error"
                )
                # Send trace activity
                await context.send_activity(trace_activity)
            nonlocal self
            await self._conversation_state.delete(context)
            
        self.on_turn_error = on_error