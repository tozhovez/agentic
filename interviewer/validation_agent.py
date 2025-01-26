import logging

from llm_client import LLMClient
from models import ValidationResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AGENT_TEMPLATE_SYSTEM = """
You are an expert interviewer with deep knowledge of various roles.
Validate the scores and provide a brief summary feedback.
Include strengths and areas for improvement.
Review the following interview evaluation:
"""

AGENT_TEMPLATE_TASK = """
Provide:
1. Validated scores from 1-10 (where 10 is excellent) (adjust if needed)
2. Overall feedback
Format your response as a JSON object with 'validated_scores' and 'feedback' fields.
"""

class ValidationAgent:
    def __init__(self):
        self.agent_client = LLMClient(
            model='llama3.2',
            options={'temperature': 0.6}
            )
        self.agent_response_format = ValidationResponse.model_json_schema()
  
    async def async_generate_response_validation(self, prompt):
        response = await self.agent_client.generate_response(
            prompt=f"{AGENT_TEMPLATE_SYSTEM}\n\n{prompt}\n\n{AGENT_TEMPLATE_TASK}",
            response_format=self.agent_response_format 
            )
        # Use Pydantic to validate the response
        response = ValidationResponse.model_validate_json(response.message.content)
        return response

