from bson import ObjectId
from typing import Any
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        """
        This method defines the Pydantic V2 validation and serialization schema.
        It allows the model to accept a string or an ObjectId and validates it.
        It also defines how to serialize the ObjectId to a string.
        """
        def validate(v):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid ObjectId")
            return ObjectId(v)

        # This schema handles validation from different sources
        # and defines serialization behavior.
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema(
                [
                    # Already an ObjectId
                    core_schema.is_instance_schema(ObjectId),
                    # A string to be converted
                    core_schema.chain_schema([core_schema.str_schema(), core_schema.no_info_plain_validator_function(validate)]),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )