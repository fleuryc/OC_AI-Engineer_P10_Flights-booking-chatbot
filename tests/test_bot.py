from logging import Manager
import aiounittest
from botbuilder.core import ConversationState, MemoryStorage, TurnContext
from botbuilder.core.adapters import TestAdapter
from botbuilder.dialogs import DialogSet, DialogTurnStatus, WaterfallDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt
from botbuilder.schema import Activity, ActivityTypes

from bot.config import DefaultConfig  # type: ignore
from bot.dialogs import BookingDialog, MainDialog  # type: ignore
from bot.flight_booking_recognizer import FlightBookingRecognizer  # type: ignore
from bot.bots import DialogAndWelcomeBot


class MainDialogTest(aiounittest.AsyncTestCase):
    async def test_main_dialog(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)
            results = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                await main_dialog.intro_step(dialog_context)

            elif results.status == DialogTurnStatus.Complete:
                reply = results.result
                await turn_context.send_activity(reply)

            await conv_state.save_changes(turn_context)

        conv_state = ConversationState(MemoryStorage())
        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)
        main_dialog = MainDialog(
            FlightBookingRecognizer(DefaultConfig()), BookingDialog()
        )
        dialogs.add(main_dialog)

        adapter = TestAdapter(exec_test)

        step1 = await adapter.test("Hello", None, timeout=30 * 1000)
