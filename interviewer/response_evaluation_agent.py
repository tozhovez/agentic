import logging

from llm_client import LLMClient
from models import EvaluationResponse, EvaluationRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


AGENT_TEMPLATE_SYSTEM = """
You are an expert interviewer with deep knowledge of various roles.
"""


AGENT_TEMPLATE_TASK = """
Evaluate the response based on relevance, completeness, clarity, job title and job description.
Provide:
1. A score from 1-10 (where 10 is excellent)
2. A brief comment explaining the score
Format and Return your score and brief comment as a JSON object with 'score' and 'comment' fields.
"""


class ResponseEvaluationAgent:
    """
    The ResponseEvaluationAgent evaluates candidate responses using an LLM.

    Attributes:
        agent_client (LLMClient): Client for interacting with the LLM.
        agent_response_format: The expected schema for evaluation responses.
    """
    def __init__(self):
        self.agent_client = LLMClient(
            model='llama3.2',
            options={'temperature': 1.0}
            )
        self.agent_response_format = EvaluationResponse.model_json_schema()


    async def async_generate_response_evaluation(
        self, job: str, evaluation: EvaluationRequest
        ):
        prompt = (
            f"Question: {evaluation.question}\n"
            f"Response: {evaluation.answer}\n\n"
            f"Candidate Response for Job Description:\n{job}"
            )
        response = await self.agent_client.generate_response(
            prompt=f"{AGENT_TEMPLATE_SYSTEM}\n\n{AGENT_TEMPLATE_TASK}\n\n{prompt}",
            response_format=self.agent_response_format
            )
        # Use Pydantic to validate the response
        response = EvaluationResponse.model_validate_json(response.message.content)
        return response
