from pydantic import BaseModel

class Job(BaseModel):
    job_title: str
    job_description: str


class InterviewRequest(BaseModel):
    candidate_id: str
    job_title: str
    job_description: str


class InterviewReportRequest(BaseModel):
    session_id: str


class InterviewSession(BaseModel):
    session_id: str
    candidate_id: str
    job_title: str
    timestamp: str
    data_path: str


# Define the schemes for the Questions
class Question(BaseModel):
    question: str


class Questions(BaseModel):
    qId: int  # Unique identifier for the question
    question: str  # The text of the question


class QuestionsStore(BaseModel):
    questions: dict  # Maps qId (key) to question (value)


class QuestionList(BaseModel):
    questions: list[Question]



# Define the schemes for the Evaluation 
class EvaluationRequest(BaseModel):
    question: str
    answer: str


class EvaluationResponse(BaseModel):
    score: int
    comment: str


class Evaluation(BaseModel):
    question: str
    answer: str
    score: int
    comment: str


class ValidationRequest(BaseModel):
    job_title: str
    evaluations: list[Evaluation]  # Each dict contains `score` and `comment`.


class ValidationResponse(BaseModel):
    validated_scores: int
    feedback: str
    
class CandidateResponse(BaseModel):
    question_id: int
    answer: str


class AnswerRequest(BaseModel):
    #job_title: str
    question: str


class AnswerResponse(BaseModel):
    answer: str
