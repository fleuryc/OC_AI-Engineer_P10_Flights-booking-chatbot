# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Flight booking dialog."""

import requests
from botbuilder.core import BotTelemetryClient, MessageFactory, NullTelemetryClient
from botbuilder.dialogs import DialogTurnResult, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import ConfirmPrompt, PromptOptions, TextPrompt
from botbuilder.schema import InputHints
from datatypes_date_time.timex import Timex

from .cancel_and_help_dialog import CancelAndHelpDialog
from .date_resolver_dialog import DateResolverDialog


class BookingDialog(CancelAndHelpDialog):
    """Flight booking implementation."""

    def __init__(
        self,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super().__init__(dialog_id or BookingDialog.__name__, telemetry_client)
        self.telemetry_client = telemetry_client
        text_prompt = TextPrompt(TextPrompt.__name__)
        text_prompt.telemetry_client = telemetry_client

        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__,
            [
                self.or_city_step,
                self.dst_city_step,
                self.str_date_step,
                self.end_date_step,
                self.budget_step,
                self.confirm_step,
                self.final_step,
            ],
        )
        waterfall_dialog.telemetry_client = telemetry_client

        self.add_dialog(text_prompt)
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            DateResolverDialog(
                DateResolverDialog.START_DATE_DIALOG_ID, self.telemetry_client
            )
        )
        self.add_dialog(
            DateResolverDialog(
                DateResolverDialog.END_DATE_DIALOG_ID, self.telemetry_client
            )
        )
        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__

    async def or_city_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for or_city."""
        booking_details = step_context.options

        if booking_details.or_city is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("🛫 Where do you want to leave from ?")
                ),
            )

        return await step_context.next(booking_details.or_city)

    async def dst_city_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for dst_city."""
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.or_city = step_context.result.capitalize()

        if booking_details.dst_city is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("🛬 Where do you want to go to ?")
                ),
            )

        return await step_context.next(booking_details.dst_city)

    async def str_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for travel date.
        This will use the DATE_RESOLVER_DIALOG."""

        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.dst_city = step_context.result.capitalize()

        if not booking_details.str_date or self.is_ambiguous(booking_details.str_date):
            return await step_context.begin_dialog(
                DateResolverDialog.START_DATE_DIALOG_ID,
                booking_details.str_date,
            )

        return await step_context.next(booking_details.str_date)

    async def end_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for travel date.
        This will use the DATE_RESOLVER_DIALOG."""

        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.str_date = step_context.result

        if not booking_details.end_date or self.is_ambiguous(booking_details.end_date):
            return await step_context.begin_dialog(
                DateResolverDialog.END_DATE_DIALOG_ID, booking_details.end_date
            )

        return await step_context.next(booking_details.end_date)

    async def budget_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for travel budget."""
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.end_date = step_context.result

        if booking_details.budget is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(
                        "💸 How much do you want to spend on this trip ?"
                    )
                ),
            )

        return await step_context.next(booking_details.budget)

    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Confirm the information the user has provided."""
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.budget = step_context.result

        distance = requests.get(
            f"https://www.distance24.org/route.json?stops={booking_details.or_city}|{booking_details.dst_city}"
        ).json()
        flight_co2_impact = requests.get(
            f"https://api.monimpacttransport.fr/beta/getEmissionsPerDistance?transportations=1&km={ distance['distance'] }"
        ).json()
        all_co2_impact = requests.get(
            f"https://api.monimpacttransport.fr/beta/getEmissionsPerDistance?filter=smart&fields=emoji&km={distance['distance']}"
        ).json()
        equivalents = requests.get(
            "https://raw.githubusercontent.com/datagir/monconvertisseurco2/1677802d89e9f1ad1678a0eb8d506c78e6f1f050/public/data/equivalents.json"
        ).json()

        msg = f"""
Please confirm your trip details :
- 🛫 from : **{ booking_details.or_city }**
- 🛬 to : **{ booking_details.dst_city }**
- 🥳 departure date : **{ booking_details.str_date }**
- 😮‍💨 return date : **{ booking_details.end_date }**
- 💸 for a budget of : **{ booking_details.budget }**

🏭 This trip will produce \
**{round(flight_co2_impact[0]['emissions']['kgco2e']*2, 2)} kg of CO2eq** \
({round(flight_co2_impact[0]['emissions']['kgco2e']*2 / 2000 * 100, 2)} % \
of your annual budget of 2000 kg)

---

As a comparison for the same distance :"""

        for transportation_mode in all_co2_impact:
            msg = (
                msg
                + f"""
- {transportation_mode['emoji']['main']} {transportation_mode['name']} : {round(transportation_mode['emissions']['kgco2e']*2, 2)} kg of CO2eq"""
            )

        msg = (
            msg
            + """

This is the equivalent of (one of) :"""
        )

        for eq in equivalents:
            msg = (
                msg
                + f"""
- {eq['emoji']} {round(flight_co2_impact[0]['emissions']['kgco2e']*2 / eq['total'])} {eq['name']['fr']}"""
            )

        msg = (
            msg
            + """
---

_sources : https://monimpacttransport.fr/ and https://monconvertisseurco2.fr/_"""
        )

        # Offer a YES/NO prompt.
        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text(
                    msg, msg, input_hint=InputHints.ignoring_input
                )
            ),
        )

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Complete the interaction and end the dialog."""

        booking_details = step_context.options

        if step_context.result:
            self.telemetry_client.track_trace(
                "booking_accepted",
                properties=booking_details.__dict__,
            )

            return await step_context.end_dialog(booking_details)

        self.telemetry_client.track_trace(
            "booking_refused",
            properties=booking_details.__dict__,
        )

        return await step_context.end_dialog()

    def is_ambiguous(self, timex: str) -> bool:
        """Ensure time is correct."""
        timex_property = Timex(timex)
        return "definite" not in timex_property.types
