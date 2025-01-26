from models import AnswerRequest, AnswerResponse
import logging
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from llm_client import LLMClient

AGENT_TEMPLATE_TASK = """
Generate an answer to the interview question.
Return the answer in text format.
"""

class AnswerAgent:
  def __init__(self):
    self.agent_client = LLMClient(
      model="llama3.2", #'granite3.1-moe'
      options={'temperature': 0.5, 'max_tokens': 50}
      )
    # Define the schema for the response
    self.agent_response_format = AnswerResponse.model_json_schema()


  async def generate_answer(self, request) -> str:
    """Business logic for generating an answer."""
    response = await self.agent_client.generate_response(
      prompt=f"The Question:\n{request.question}\n\n{AGENT_TEMPLATE_TASK}",
      response_format=self.agent_response_format
      )
    # Use Pydantic to validate the response
    response = AnswerResponse.model_validate_json(response.message.content)
    return response
