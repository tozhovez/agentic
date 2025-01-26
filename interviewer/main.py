"""
Main module for the interviewer FastAPI application.

This module initializes the FastAPI app, defines routes for managing interview sessions,
and orchestrates the interview process using the InterviewManager and ReportManager classes.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from models import InterviewRequest, CandidateResponse, InterviewReportRequest
from interview import InterviewManager
from reports import ReportManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

report_manager = ReportManager()
interview_manager = InterviewManager()

# Routes
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for managing the application's lifecycle.
    This function is called when the application starts and stops.
    It initializes the database connection on startup and handles any cleanup on shutdown.
    """
    await interview_manager.db.init_db()
    yield
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

@app.post("/interviews/start")
async def start_interview(request: InterviewRequest):
    """
    Start a new interview session.

    Args:
        request (InterviewRequest):
                The request containing the candidate's job title and details.

    Returns:
        dict: The initial set of interview questions and session details.
    """
    print(request)
    return await interview_manager.start_interview(request)

@app.post("/interviews/{session_id}/respond")
async def submit_response(session_id: str, response: CandidateResponse):
    """
    Submit a response to an ongoing interview session.

    Args:
        session_id (str): The unique identifier for the interview session.
        response (CandidateResponse): The candidate's response to a question.

    Returns:
        dict: The updated session data, including evaluated responses and scores.
    """
    return await interview_manager.candidate_answer(session_id, response)

@app.post("/reports")
async def summary_report(request: InterviewReportRequest):
    """
    Generate a summary report for an interview session.

    Args:
        request (InterviewReportRequest):
                The request containing the session ID and report preferences.

    Returns:
        dict: The summary report containing questions, responses, scores, and feedback.
    """
    return await report_manager.get_summary_report(request)

@app.post("/log")
async def session_log():
    """
    Retrieve the session logs.

    Returns:
        dict: The session logs, including candidate details,
              timestamps, and file paths for saved data.
    """
    return await report_manager.get_session_log()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8765)
    
    

