"""
This module defines the InterviewManager class, which orchestrates
the management of interview sessions, question generation, response
evaluation, and result validation. It integrates with multiple agents
and handles the entire interview lifecycle.
"""
import uuid
import json
from datetime import datetime
import logging
from fastapi import HTTPException
from database import Database
from models import (
    InterviewRequest, CandidateResponse, EvaluationRequest, InterviewSession
    )
from question_agent import QuestionAgent
from response_evaluation_agent import ResponseEvaluationAgent
from validation_agent import ValidationAgent
from storage import StorageManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
    Manages the interview process by coordinating the generation of
    questions, evaluation of responses, and validation of results. It
    stores session data and interacts with external agents for various
    functionalities.
"""

class InterviewManager:
    def __init__(self):
        """Initializes the InterviewManager with required agents and storage."""
        self.question_agent = QuestionAgent()
        self.evaluation_agent = ResponseEvaluationAgent()
        self.validation_agent = ValidationAgent()
        self.storage = StorageManager()
        self.db = Database()
        self.sessions = {}

    async def generate_questions(self, session_id: str):
        """
        Generates interview questions based on the job title and description
        of the session.

        Args:
            session_id (str): The unique identifier of the interview session.

        Returns:
            dict: A dictionary mapping question IDs to questions.
        """
        if session_id not in self.sessions:
            raise HTTPException(status_code=404, detail="Session not found")

        role = str(
            f"{self.sessions[session_id]['job_title']}\n"
            f"{self.sessions[session_id]['job_description']}"
            )

        interview_questions = await self.question_agent.async_generate_questions(role)

        # Output the generated questions
        for i, question_obj in enumerate(interview_questions, start=1):
            print(f"Question {i}: {question_obj.question}")

        question_data = {i: q_obj.question for i, q_obj in enumerate(
            interview_questions, start=1
            )}

        return question_data


    async def start_interview(self, request: InterviewRequest) -> dict:
        """Initialize an interview session."""

        session_id = str(uuid.uuid4())

        session_data = {
            "session_id": session_id,
            "candidate_id": request.candidate_id,
            "job_title": request.job_title,
            "job_description": request.job_description,
            "timestamp": datetime.now().isoformat(),
            "data_path": f"{self.storage.path}/{session_id}.json",
            "questions": {},
            "answers": {},
            "evaluations": {},
            "validation": {}
            }
        self.sessions[session_id] = session_data
        #await self.storage.store_into_redis(session_id, session_data)
        questions = await self.generate_questions(session_id)
        self.sessions[session_id]["questions"] = questions
        #await self.storage.store_questions_in_redis(session_id, questions)
        return {"session_id": session_id, "questions": questions}


    async def candidate_answer(self, session_id: str, response: CandidateResponse) -> dict:
        if session_id not in self.sessions:
            raise HTTPException(status_code=404, detail="Session not found")

        self.sessions[session_id]["answers"][response.question_id] = response.answer

        evaluation_request = EvaluationRequest.model_validate_json(json.dumps({
            'question': self.sessions[session_id]["questions"][response.question_id],
            'answer': response.answer
            }))

        job = str(
            f"{self.sessions[session_id]['job_title']}\n"
            f"{self.sessions[session_id]['job_description']}"
            )

        eval_response = await self.evaluation_agent.async_generate_response_evaluation(
                job, evaluation_request
                )
        print(
            f"score: {eval_response.score}"
            f"comment: {eval_response.comment}"
            )
        self.sessions[session_id]["evaluations"][response.question_id] = {
            'score': eval_response.score,
            'comment': eval_response.comment
            }


        if len(self.sessions[session_id]["answers"]) == len(
            self.sessions[session_id]["questions"]
            ):
            return await self.complete_interview(session_id)
        return {"status": "response_recorded"}


    async def complete_interview(self, session_id) -> dict:
        """
        Finalizes the interview by compiling answers, evaluations, and 
        validation results. Stores the data and generates a final report.

        Args:
            session_id (str): The unique identifier of the interview session.

        Returns:
            dict: The final report containing all interview data.
        """
        if session_id not in self.sessions:
            raise HTTPException(status_code=404, detail="Session not found")

        data = []
        for k, _ in enumerate(range(len(self.sessions[session_id]["answers"])), start=1):
            text = str(
                f"question {k}: {self.sessions[session_id]['questions'][k]}\n"
                f"answer   {k}: {self.sessions[session_id]['answers'][k]}\n"
                f"score    {k}: {self.sessions[session_id]['evaluations'][k]['score']}\n"
                f"comment  {k}: {self.sessions[session_id]['evaluations'][k]['comment']}\n"
            )
            data.append(f"The Interview Question {k}:\n{text}\n\n")

        data_result = str(
            f'Job Title: {self.sessions[session_id]["job_title"]}\n'
            f'Job Description: {self.sessions[session_id]["job_description"]}\n\n\n'
            f'{"\n".join(data)}'
            )
        print(data_result)
        try:
            validation = await self.validation_agent.async_generate_response_validation(
                data_result
                )

            self.sessions[session_id]["validation"] = {
                "summary_score":validation.validated_scores,
                "feedback": validation.feedback
                }

            print(self.sessions[session_id]["data_path"])

            # Prepare final report
            final_report = {
                "candidate_id": self.sessions[session_id]["candidate_id"],
                "job_title": self.sessions[session_id]["job_title"],
                "questions_and_answers": [
                    {
                        "question": self.sessions[session_id]["questions"].get(i),
                        "response": self.sessions[session_id]["answers"].get(i),
                        "evaluation": self.sessions[session_id]["evaluations"].get(i),
                    }
                    for i, q in enumerate(self.sessions[session_id]["questions"])
                ],
                "final_score": validation.validated_scores,
                "feedback": validation.feedback
            }

            # Save to storage
            await self.storage.save_interview_data(
                self.sessions[session_id]["data_path"],
                final_report
                )

            # Log session
            session_log = InterviewSession(
                session_id=session_id,
                candidate_id=self.sessions[session_id]["candidate_id"],
                job_title=self.sessions[session_id]["job_title"],
                timestamp=self.sessions[session_id]["timestamp"],
                data_path=self.sessions[session_id]["data_path"]
            )
            print(session_log)
            await self.db.save_session(session_log)

            # Cleanup session
            del self.sessions[session_id]
            print(final_report)
            return final_report
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error validating scores: {e}")
