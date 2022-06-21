"""Main dialog to welcome users."""
import json
import os.path
from typing import List

from botbuilder.core import (
    BotTelemetryClient,
    ConversationState,
    TurnContext,
    UserState,
)
from botbuilder.dialogs import Dialog
from botbuilder.schema import Activity, Attachment, ChannelAccount
from helpers.activity_helper import create_activity_reply

from .dialog_bot import DialogBot


class DialogAndWelcomeBot(DialogBot):
    """Main dialog to welcome users."""

    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
        telemetry_client: BotTelemetryClient,
    ):
        """Initialize the bot."""
        super().__init__(conversation_state, user_state, dialog, telemetry_client)
        self.telemetry_client = telemetry_client

    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):
        """
        Send a welcome message to the user when they join the conversation.
        :param members_added: The members added to the conversation.
        :param turn_context: The context object for the turn.
        """

        for member in members_added:
            # Greet anyone that was not the target (recipient) of this message.
            # To learn more about Adaptive Cards, see https://aka.ms/msbot-adaptivecards
            # for more details.
            if member.id != turn_context.activity.recipient.id:
                welcome_card = DialogAndWelcomeBot.create_adaptive_card_attachment()
                response = DialogAndWelcomeBot.create_response(
                    turn_context.activity, welcome_card
                )
                await turn_context.send_activity(response)

    @staticmethod
    def create_response(activity: Activity, attachment: Attachment):
        """Create an attachment message response."""
        response = create_activity_reply(activity)
        response.attachments = [attachment]
        return response

    @staticmethod
    def create_adaptive_card_attachment():
        """Create an adaptive card."""
        relative_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(relative_path, "resources/welcomeCard.json")
        with open(path, encoding="utf-8") as card_file:
            card = json.load(card_file)

        return Attachment(
            content_type="application/vnd.microsoft.card.adaptive", content=card
        )
