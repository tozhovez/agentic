from pydantic import BaseModel

class AnswerRequest(BaseModel):
    #job_title: str
    question: str

class AnswerResponse(BaseModel):
    answer: str

