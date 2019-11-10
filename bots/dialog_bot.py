from botbuilder.core import ActivityHandler, ConversationState, TurnContext, UserState
from botbuilder.schema import ChannelAccount
from botbuilder.dialogs import Dialog
from helpers.dialog_helper import DialogHelper

from data_models import WelcomeUserState

#The ConversationState is used by the Dialog system. The UserState isn't
class DialogBot(ActivityHandler):
    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState
    ):
        if conversation_state is None:
            raise TypeError(
                "[DialogBot]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                "[DialogBot]: Missing parameter. user_state is required but None was given"
            )

        self.conversation_state = conversation_state
        self.user_state = user_state
        self.user_state_accessor = self.user_state.create_property('WelcomeUserState')

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        welcome_user_state = await self.user_state_accessor.get(turn_context, WelcomeUserState)

        if not welcome_user_state.did_welcome_user:
            welcome_user_state.did_welcome_user = True
            name = turn_context.activity.from_property.name
            await turn_context.send_activity(f"Welcome { name }")
        else:
            text = turn_context.activity.text.lower()
            await turn_context.send_activity(f"You said: {text}")
    
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    f" Hi there {member.name}"
                )