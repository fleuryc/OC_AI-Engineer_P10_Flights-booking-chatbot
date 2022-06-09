# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from typing import Dict, Final, List, Optional, Tuple

from booking_details import BookingDetails
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import TurnContext


class LuisConstants:
    """Constants to be used in the LUIS examples."""

    BOOK_INTENT: Final[str] = "Book"
    INFO_INTENT: Final[str] = "Info"
    NONE_INTENT: Final[str] = "None"

    NOT_NONE_INTENTS: Final[List[str]] = [BOOK_INTENT, INFO_INTENT]
    ALL_INTENTS: Final[List[str]] = [BOOK_INTENT, INFO_INTENT, NONE_INTENT]

    ORIGIN_CITY_ENTITY: Final[str] = "or_city"
    DESTINATION_CITY_ENTITY: Final[str] = "dst_city"
    START_DATE_ENTITY: Final[str] = "str_date"
    END_DATE_ENTITY: Final[str] = "end_date"
    BUDGET_ENTITY: Final[str] = "budget"

    LOCATION_ENTITIES: Final[List[str]] = [
        ORIGIN_CITY_ENTITY,
        DESTINATION_CITY_ENTITY,
    ]
    LOCATION_TYPE: Final[str] = "geographyV2_city"

    DATE_ENTITIES: Final[List[str]] = [START_DATE_ENTITY, END_DATE_ENTITY]
    DATE_TYPE: Final[str] = "datetime"

    QUANTITY_ENTITIES: Final[List[str]] = [BUDGET_ENTITY]
    QUANTITY_TYPE: Final[str] = "number"

    ALL_ENTITIES: Final[Dict[str, str]] = {
        ORIGIN_CITY_ENTITY: LOCATION_TYPE,
        DESTINATION_CITY_ENTITY: LOCATION_TYPE,
        START_DATE_ENTITY: DATE_TYPE,
        END_DATE_ENTITY: DATE_TYPE,
        BUDGET_ENTITY: QUANTITY_TYPE,
    }
    ALL_TYPES: Final[Dict[str, List[str]]] = {
        LOCATION_TYPE: LOCATION_ENTITIES,
        DATE_TYPE: DATE_ENTITIES,
        QUANTITY_TYPE: QUANTITY_ENTITIES,
    }


class LuisHelper:
    @staticmethod
    async def execute_luis_query(
        luis_recognizer: LuisRecognizer, turn_context: TurnContext
    ) -> Tuple[Optional[str], Optional[BookingDetails]]:
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        intent = None
        result = None

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)
            intent = recognizer_result.get_top_scoring_intent().intent

            if intent in LuisConstants.NOT_NONE_INTENTS:
                result = BookingDetails()

                for (
                    entity_name,
                    entity_type,
                ) in LuisConstants.ALL_ENTITIES.items():
                    top_entity = await LuisHelper.get_top_entity(
                        recognizer_result, entity_name, entity_type
                    )

                    if top_entity is not None:
                        setattr(
                            result,
                            entity_name,
                            top_entity,
                        )

        except Exception as exception:
            print(exception)

        return intent, result

    @staticmethod
    async def get_top_entity(
        recognizer_result: LuisRecognizer, entity_name: str, entity_type: str
    ) -> Optional[str]:
        """
        Returns the top entity from the LUIS results.
        """

        if (
            recognizer_result.entities.get("$instance") is None
            or recognizer_result.entities.get(entity_name) is None
            or len(recognizer_result.entities.get(entity_name)) == 0
        ):
            return None

        recognized_entity = recognizer_result.entities.get("$instance").get(
            entity_name
        )[0]

        top_score = 0
        top_index = None

        for index, entity in enumerate(
            recognizer_result.entities.get("$instance").get(entity_type)
        ):
            score = min(entity["endIndex"], recognized_entity["endIndex"]) - max(
                entity["startIndex"], recognized_entity["startIndex"]
            )

            if score > top_score:
                top_index = index
                top_score = score

        if (
            top_index is None
            or recognizer_result.entities.get(entity_type) is None
            or len(recognizer_result.entities.get(entity_type)) < top_index
        ):
            return None

        return (
            recognizer_result.entities.get(entity_type)[top_index].capitalize()
            if entity_type == LuisConstants.LOCATION_TYPE
            else recognizer_result.entities.get(entity_type)[top_index]["timex"][0]
            if entity_type == LuisConstants.DATE_TYPE
            else f"${recognizer_result.entities.get(entity_type)[top_index]}"
            if entity_type == LuisConstants.QUANTITY_TYPE
            else None
        )
