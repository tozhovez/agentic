"""
This module defines the QuestionAgent class for generating interview
questions using a local Language Learning Model (LLM).
"""
import logging
from models import QuestionList

from llm_client import LLMClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AGENT_TEMPLATE_SYSTEM = """
You are an expert interviewer with deep knowledge of various roles.
"""

AGENT_TEMPLATE_TASK = """
Generate three interview questions
for a candidate based on the following job title and job description.
Return a list of questions in JSON format.
"""

class QuestionAgent:
    """
    An agent for generating role-specific interview questions
    using an LLM.

    Attributes:
        agent_client (LLMClient): The client for communicating with the LLM.
        agent_response_format (dict): The schema for validating the generated response.
    """
    def __init__(self):
        self.agent_client = LLMClient(
            model='llama3.2', #'granite3.1-moe'
            options={'temperature': 0.0}
            )
        self.agent_response_format = QuestionList.model_json_schema()


    async def async_generate_questions(self, role_description: str):
        response = await self.agent_client.generate_response(
            prompt=str(
                f"{AGENT_TEMPLATE_SYSTEM}\n\n"
                f"{AGENT_TEMPLATE_TASK}\n\n"
                f"{role_description}"
                ),
            # Use Pydantic to generate the schema
            response_format=self.agent_response_format
            )
        # Use Pydantic to validate the response
        questions_response = QuestionList.model_validate_json(response.message.content)
        return questions_response.questions
