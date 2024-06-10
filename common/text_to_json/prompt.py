from typing import Callable, Tuple, Union
from dotenv import load_dotenv
from langchain_core.outputs.generation import Generation
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel

load_dotenv()


# JSON Parser
def create_pydantic_parser(
    model: BaseModel = None,
) -> Tuple[Callable[[AIMessage], Union[AIMessage, str]], str]:
    try:
        json_parser = JsonOutputParser(pydantic_object=model)
    except Exception as e:
        return f"create_pydantic_parser: Failed to create JsonOutputParser. Error: {e}"

    def pydantic_parser(ai_message: AIMessage) -> Union[AIMessage, str]:
        try:
            total_tokens = ai_message.response_metadata["token_usage"]["total_tokens"]
            # print(f"total_tokens: {total_tokens}")
            finish_reason = ai_message.response_metadata["finish_reason"]
            if finish_reason == "stop":
                # print(f"ai raw output: {ai_message.content}")
                try:
                    content = ai_message.content.strip()
                    ai_message.content = json_parser.parse_result(
                        [Generation(text=content)]
                    )
                except Exception as e:
                    return f"pydantic_parser: failed parsing to json. Error: {e}"

                return ai_message
            elif finish_reason == "tool_calls":
                print(f"parser tool: {ai_message.tool_calls}")
                return ai_message
            else:
                return f"pydantic_parser: finish_reason not handled. finish_reason: {finish_reason}"
        except Exception as e:
            return f"pydantic_parser unknown error: {e}"

    return (
        pydantic_parser,
        json_parser.get_format_instructions()
        + "\nDo not include any preamble or explanation in the response.",
    )


# llama3 instruct template
from langchain_core.prompts import PromptTemplate

llama3StartConversation = PromptTemplate.from_template(
    """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{system_message}\n{format_instructions}\n<|eot_id|><|start_header_id|>user<|end_header_id|>
{user_message}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
)


# Prompt
from langchain_groq import ChatGroq
from langchain_core.pydantic_v1 import BaseModel
import os
from typing import Type, Union, TypeVar

T = TypeVar("T", bound=BaseModel)
model_name = os.getenv("GROQ_MODEL", "llama3-70b-8192")
groq_api_key = os.getenv("GROQ_API_KEY")


def prompt_llama3_to_json(
    system_message: str,
    user_message: str,
    model: Type[T],
) -> Union[T, str]:
    llm = ChatGroq(
        temperature=0, model_name=model_name, verbose=True, api_key=groq_api_key
    )
    parser, format_instructions = create_pydantic_parser(model)
    chain = llama3StartConversation | llm | parser
    try:
        input = {
            "system_message": system_message,
            "format_instructions": format_instructions,
            "user_message": user_message,
        }

        # Log prompt for testing:
        # final_prompt = llama3StartConversation.format(**input)
        # print(f"formatted prompt: {final_prompt}")
        result = chain.invoke(input)

        return model(**result.content)
    except Exception as e:
        return f"prompt_llama3_to_json unknown error: {e}"