import json

import aiounittest
from botbuilder.core import ConversationState, MemoryStorage, TurnContext
from botbuilder.core.adapters import TestAdapter
from botbuilder.dialogs import DialogSet, DialogTurnStatus
from botbuilder.dialogs.prompts import TextPrompt

from bot.booking_details import BookingDetails  # type: ignore
from bot.config import DefaultConfig  # type: ignore
from bot.dialogs import BookingDialog, MainDialog  # type: ignore
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
            "I want leave on the first of January 2023 and come back on the \
                17th of january 2023.",
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


class MainDialogTest(aiounittest.AsyncTestCase):
    async def test_booking_dialog(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)
            results = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                await main_dialog.intro_step(dialog_context)

            elif results.status == DialogTurnStatus.Complete:
                await main_dialog.act_step(dialog_context)

            await conv_state.save_changes(turn_context)

        conv_state = ConversationState(MemoryStorage())
        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)
        booking_dialog = BookingDialog()
        main_dialog = MainDialog(
            FlightBookingRecognizer(DefaultConfig()), booking_dialog
        )
        dialogs.add(booking_dialog)

        text_prompt = await main_dialog.find_dialog(TextPrompt.__name__)
        dialogs.add(text_prompt)

        wf_dialog = await main_dialog.find_dialog(MainDialog.INITIAL_DIALOG_ID)
        dialogs.add(wf_dialog)

        adapter = TestAdapter(exec_test)

        await adapter.test("Hi!", "Hello there ! What can I help you with today?")

        await adapter.test("Book a flight", "🛫 Where do you want to leave from ?")
        await adapter.test("Paris", "🛬 Where do you want to go to ?")
        await adapter.test("London", "When do you want to leave 🥳 ?")
        await adapter.test(
            "First of January 2023",
            "I'm sorry, for best results, please enter your travel date including the month, day and year.",
        )
        await adapter.test("2023-01-01", "When will you be coming back 😮‍💨 ?")
        await adapter.test(
            "2023-01-17",
            "💸 How much do you want to spend on this trip ?",
        )
        await adapter.test(
            "$100",
            """Please confirm your trip details :
- 🛫 from : **Paris**
- 🛬 to : **London**
- 🥳 departure date : **2023-01-01**
- 😮‍💨 return date : **2023-01-17**
- 💸 for a budget of : **$100**

🏭 This trip will produce **158.24 kg of CO2eq** (7.91 % of your annual budget of 2000 kg)

---

As a comparison for the same distance :
- 🚄 TGV : 1.19 kg of CO2eq
- 🚈 Intercités : 3.64 kg of CO2eq
- 🚗 Voiture (thermique) : 132.78 kg of CO2eq
- 🚗 Voiture (électrique) : 13.62 kg of CO2eq
- 🚌 Autocar : 24.22 kg of CO2eq
- 🏍️ Moto : 115.58 kg of CO2eq

This is the equivalent of (one of) :
- 🍔 22 Repas avec du boeuf
- 🍎 310 Repas végétarien
- 🏘️ 8 Jour[s] de chauffage (gaz)
- 🚗 820 km en voiture
- 🚅 91468 km en TGV
- 📱 5 Smartphone[s]
- 👖 7 Jean[s] en coton
- 📚 134 Livre[s] de poche
- 🛋 1 Canapé[s] convertible[s]
- 👕 30 T-shirt[s] en coton
- ✈️ 851 km en avion
- 🍗 100 Repas avec du poulet
- 📺 0 Télévision[s] 45 pouces
- 💻 1 Ordinateur[s] portable[s]
- 🖥️ 1 Ecran[s] d'ordinateur 23,8 pouces
- 📄 34550 Feuille[s] de papier A4
- 🚮 410 kg d'ordures ménagères
- 🚰 1198788 Litre[s] d'eau du robinet
- 💧 349 Litre[s] d'eau en bouteille
---

_sources : https://monimpacttransport.fr/ and https://monconvertisseurco2.fr/_ (1) Yes or (2) No""",
        )

    async def test_luis_dialog(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)
            results = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                await main_dialog.intro_step(dialog_context)

            elif results.status == DialogTurnStatus.Complete:
                await main_dialog.act_step(dialog_context)

            await conv_state.save_changes(turn_context)

        conv_state = ConversationState(MemoryStorage())
        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)
        booking_dialog = BookingDialog()
        main_dialog = MainDialog(
            FlightBookingRecognizer(DefaultConfig()), booking_dialog
        )
        dialogs.add(booking_dialog)

        text_prompt = await main_dialog.find_dialog(TextPrompt.__name__)
        dialogs.add(text_prompt)

        wf_dialog = await main_dialog.find_dialog(MainDialog.INITIAL_DIALOG_ID)
        dialogs.add(wf_dialog)

        adapter = TestAdapter(exec_test)

        await adapter.test("Hi!", "Hello there ! What can I help you with today?")

        await adapter.test(
            "I want to book a trip from Paris to London for less than $100. \
                I will leave on the first of January 2023 and \
                    come back on the 17th of january 2023.",
            """Please confirm your trip details :
- 🛫 from : **Paris**
- 🛬 to : **London**
- 🥳 departure date : **2023-01-01**
- 😮‍💨 return date : **2023-01-17**
- 💸 for a budget of : **$100**

🏭 This trip will produce **158.24 kg of CO2eq** (7.91 % of your annual budget of 2000 kg)

---

As a comparison for the same distance :
- 🚄 TGV : 1.19 kg of CO2eq
- 🚈 Intercités : 3.64 kg of CO2eq
- 🚗 Voiture (thermique) : 132.78 kg of CO2eq
- 🚗 Voiture (électrique) : 13.62 kg of CO2eq
- 🚌 Autocar : 24.22 kg of CO2eq
- 🏍️ Moto : 115.58 kg of CO2eq

This is the equivalent of (one of) :
- 🍔 22 Repas avec du boeuf
- 🍎 310 Repas végétarien
- 🏘️ 8 Jour[s] de chauffage (gaz)
- 🚗 820 km en voiture
- 🚅 91468 km en TGV
- 📱 5 Smartphone[s]
- 👖 7 Jean[s] en coton
- 📚 134 Livre[s] de poche
- 🛋 1 Canapé[s] convertible[s]
- 👕 30 T-shirt[s] en coton
- ✈️ 851 km en avion
- 🍗 100 Repas avec du poulet
- 📺 0 Télévision[s] 45 pouces
- 💻 1 Ordinateur[s] portable[s]
- 🖥️ 1 Ecran[s] d'ordinateur 23,8 pouces
- 📄 34550 Feuille[s] de papier A4
- 🚮 410 kg d'ordures ménagères
- 🚰 1198788 Litre[s] d'eau du robinet
- 💧 349 Litre[s] d'eau en bouteille
---

_sources : https://monimpacttransport.fr/ and https://monconvertisseurco2.fr/_ (1) Yes or (2) No""",
        )
