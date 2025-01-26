import httpx
import asyncio
from pprint import pprint as print
from test_data import test_data
from answer_agent import AnswerAgent
import asyncio
import logging
import json

from models import AnswerRequest, AnswerResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def post_interview_start(data):
    url = "http://localhost:8765/interviews/start"

    headers = {"Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=httpx.Timeout(300.0)) as client:
        response = await client.post(url, json=data, headers=headers)
        return response.json()



async def submit_answer(session_id, data):

    url = f"http://localhost:8765/interviews/{session_id}/respond"

    headers = {"Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=httpx.Timeout(600.0)) as client:
        response = await client.post(url, json=data, headers=headers)
        return response.json()





async def runner():
    # Run the async function
    answer_agent = AnswerAgent()

    for data in test_data:

        interview = await post_interview_start(data)
        print(interview)

        print(interview['questions'])
        for question_id in interview['questions']:
            print(question_id)
            print(interview['questions'][question_id])
            request = AnswerRequest.model_validate_json(
                json.dumps({'question': interview['questions'][question_id]})
                )
            print(request)
            answer = await answer_agent.generate_answer(request)
            print(answer)
            r = await submit_answer(
                interview['session_id'],
                {'question_id': question_id, 'answer': answer.answer}
                )
            print(f"Answer: {question_id}, {answer}")
            print(r)


asyncio.run(runner())






