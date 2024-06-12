from langchain_core.pydantic_v1 import BaseModel
from langchain_groq import ChatGroq
import os
from typing import TypeVar, Type, Union, Generic
import traceback

T = TypeVar("T", bound=BaseModel)


class TextToModel(Generic[T]):
    """
    A class that uses a Pydantic model to generate structured output from text.

    This class requires the following environment variables:
    - GROQ_API_KEY: The API key for GROQ.
    - GROQ_MODEL: The name of the GROQ model to use. If not provided, "llama3-70b-8192" will be used.

    Attributes:
        pydantic_model (Type[T]): The Pydantic model to use for structuring the output.
        model_name (str): The name of the GROQ model to use.
        structured_output_llm (ChatGroq): The ChatGroq object with structured output.
    """

    def __init__(self, pydantic_model: Type[T]):
        """
        The constructor for TextToModel class.

        Parameters:
            pydantic_model (Type[T]): The Pydantic model to use for structuring the output.
        """
        self.pydantic_model = pydantic_model
        self.model_name = os.getenv("GROQ_MODEL", "llama3-70b-8192")
        llm = ChatGroq(temperature=0, model_name=self.model_name)
        self.structured_output_llm = llm.with_structured_output(pydantic_model)

    def generate_model(self, input_text: str) -> Union[T, str]:
        """
        Generate a model from the input text.

        Parameters:
            input_text (str): The input text to generate the model from.

        Returns:
            Union[T, str]: The generated model if successful, otherwise an error message.
        """
        try:
            generated_model = self.structured_output_llm.invoke(input_text)

            if not isinstance(generated_model, self.pydantic_model):
                raise TypeError(
                    f"Expected type: {type(self.pydantic_model).__name__}, got: {type(generated_model).__name__}"
                )

            return generated_model
        except Exception as e:
            error_info = f"Exception type: {type(e).__name__}, Message: {str(e)}, Traceback: {traceback.format_exc()}"
            return error_info
