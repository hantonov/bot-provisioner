from botbuilder.core import ActivityHandler, ConversationState, TurnContext, UserState
from botbuilder.schema import ChannelAccount
from botbuilder.dialogs import Dialog
from ..helpers.dialog_helper import DialogHelper

from ..data_models import WelcomeUserState

#The ConversationState is used by the Dialog system. The UserState isn't
class DialogBot(ActivityHandler):
    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog
    ):
        if conversation_state is None:
            raise TypeError(
                "[DialogBot]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                "[DialogBot]: Missing parameter. user_state is required but None was given"
            )
        if dialog is None:
            raise Exception("[DialogBot]: Missing parameter. dialog is required")

        self.conversation_state = conversation_state
        self.user_state = user_state
        self.user_state_accessor = self.user_state.create_property('WelcomeUserState')
        self.dialog = dialog

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState")
        )
    
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    f" Thanks for joining {member.name}"
                )