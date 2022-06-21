"""Interface for flight booking recognizer."""

from botbuilder.ai.luis import LuisApplication, LuisPredictionOptions, LuisRecognizer
from botbuilder.core import (
    BotTelemetryClient,
    NullTelemetryClient,
    Recognizer,
    RecognizerResult,
    TurnContext,
)
from config import DefaultConfig


class FlightBookingRecognizer(Recognizer):
    """
    Flight booking recognizer.
    """

    def __init__(
        self, configuration: DefaultConfig, telemetry_client: BotTelemetryClient = None
    ):
        """
        Initializes a new instance of the FlightBookingRecognizer class.
        :param configuration: The configuration to use.
        :param telemetry_client: The telemetry client to use.
        """

        self._recognizer = None

        luis_is_configured = (
            configuration.LUIS_APP_ID
            and configuration.LUIS_API_KEY
            and configuration.LUIS_API_HOST_NAME
        )
        if luis_is_configured:
            # Set the recognizer options depending on which endpoint version you want to use e.g v2 or v3.
            # More details can be found in https://docs.microsoft.com/azure/cognitive-services/luis/luis-migration-api-v3
            luis_application = LuisApplication(
                configuration.LUIS_APP_ID,
                configuration.LUIS_API_KEY,
                "https://" + configuration.LUIS_API_HOST_NAME,
            )

            options = LuisPredictionOptions()
            options.telemetry_client = telemetry_client or NullTelemetryClient()

            self._recognizer = LuisRecognizer(
                luis_application, prediction_options=options
            )

    @property
    def is_configured(self) -> bool:
        """
        Checks whether the LUIS application is configured.
        :return: A boolean representing whether LUIS is configured.
        """
        # Returns true if luis is configured in the config.py and initialized.
        return self._recognizer is not None

    async def recognize(self, turn_context: TurnContext) -> RecognizerResult:
        """
        Recognizes the intent from an incoming message.
        :param turn_context: The context object for this turn.
        :return: A LuisRecognizerResult.
        """
        return await self._recognizer.recognize(turn_context)  # type: ignore
