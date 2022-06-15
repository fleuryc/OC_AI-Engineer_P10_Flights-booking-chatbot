import json

import aiounittest
from botbuilder.core import TurnContext
from botbuilder.core.adapters import TestAdapter

from bot.booking_details import BookingDetails  # type: ignore
from bot.config import DefaultConfig  # type: ignore
from bot.flight_booking_recognizer import FlightBookingRecognizer  # type: ignore
from bot.helpers.luis_helper import LuisConstants, LuisHelper  # type: ignore


class TestLuisHelper(aiounittest.AsyncTestCase):
    async def test_execute_luis_query(self):
        CONFIG = DefaultConfig()
        RECOGNIZER = FlightBookingRecognizer(CONFIG)

        async def exec_test(turn_context: TurnContext):
            # Call LUIS and gather any potential booking details. (Note the TurnContext has the response to the prompt.)
            intent, luis_result = await LuisHelper.execute_luis_query(
                RECOGNIZER, turn_context
            )
            await turn_context.send_activity(
                json.dumps(
                    {
                        "intent": intent,
                        "booking_details": luis_result.__dict__,
                    }
                )
            )

        adapter = TestAdapter(exec_test)

        await adapter.test(
            "Hello",
            json.dumps(
                {
                    "intent": LuisConstants.INFO_INTENT,
                    "booking_details": BookingDetails().__dict__,
                }
            ),
        )

        await adapter.test(
            "I want to go from Paris to London.",
            json.dumps(
                {
                    "intent": LuisConstants.BOOK_INTENT,
                    "booking_details": BookingDetails(
                        or_city="Paris",
                        dst_city="London",
                    ).__dict__,
                }
            ),
        )

        await adapter.test(
            "I want leave on the first of January 2023 and come back on the 17th of january 2023.",
            json.dumps(
                {
                    "intent": LuisConstants.INFO_INTENT,
                    "booking_details": BookingDetails(
                        str_date="2023-01-01",
                        end_date="2023-01-17",
                    ).__dict__,
                }
            ),
        )

        await adapter.test(
            "The trip should cost less than $100.",
            json.dumps(
                {
                    "intent": LuisConstants.INFO_INTENT,
                    "booking_details": BookingDetails(
                        budget="$100",
                    ).__dict__,
                }
            ),
        )
