# AI-Driven Interview System: 1-Day Prototype

## Goal
Build a minimal prototype of an AI-Driven Interview System that:
- Dynamically generates a small set of interview questions.
- Evaluates and scores the candidate’s responses.
- Produces basic feedback.

## 1. Agents
- Question Agent:
    - Generates three interview questions based on a given job description.
- Response Evaluation Agent:
    - Receives the candidate’s responses and assigns a score to each.
- Validation Agent:
    - Validates the scores from the Response Evaluation Agent.
    - Produces final feedback and summary.

## 2. Workflow
- Question Agent
    - Generates 3 questions dynamically (e.g., “What is your experience with X?”).
- Candidate
     - Provides responses to these questions.
- Response Evaluation Agent
    - Analyzes each response, assigns a score (e.g., 1–5), and notes brief comments.
- Validation Agent
    - Confirms or adjusts the scores.

Outputs a short summary report with:
- Questions
- Responses
- Scores
- Feedback


## 3. Shared Context
Store basic context such as:
- Candidate’s job title/role (e.g., “Backend Developer”).
- Current question and past responses.
Use any simple method (in-memory dictionary, small DB) for storing and retrieving this context.



## 1. System Requirements:
- (no using GPU only CPU) RAM 16G - slow running, RAM 32G  - optimal
- OS Linux Ubuntu 24.04 with installed: docker (sudoless), docker-compose (sudoless), make, git, curl, wget
if not installed:
#### To Install:
```bash
sudo apt install git wget curl
```
#### How to install docker engine:
- [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/) 

- [Linux post-installation steps for Docker Engine](https://docs.docker.com/engine/install/linux-postinstall/)


## 2. Clone git hub repo:
``` bash
git clone https://github.com/tozhovez/agentic.git
cd agentic
```

## 3. Setup Infrastructure on docker-compose:
```bash
make run-infra
```

## 4. Install local LLM on ollama:
```bash
make setup-llm
```

## 5. To Start Interviewer service (the AI-Driven Interview):
```bash
make run-interviewer
```
Interviewer service running on http://0.0.0.0:8765  and FastAPI - Swagger UI: http://0.0.0.0:8765/docs

## 6. To test the AI-Driven Interview run the candidate python 3.13.0(or dev) script into new terminal
```bash
make install-requirements
make start-candidate
```

- python 3.13.0 or dev
if it's not installed:
#### Step 1: Check Existing Python Version
Run the following command to check if Python 3.13 is already installed:
```bash
  python3 --version
```
If Python 3.13 is not listed, proceed to the next step.

#### Step 2: Install Python 3.13
For Linux (Ubuntu/Debian)
- 1. Add Python's PPA (Personal Package Archive):
```bash
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
```
- 2. Install Python 3.13:
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev -y
```

#### Step 3: Create a Virtual Environment
Once Python 3.13 is installed, create a virtual environment:
Create the environment:
```bash
python3.13 -m venv my_env
source my_env/bin/activate
```
#### Step 4: Install Required Packages
Within the virtual environment, you can now install packages using pip:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
#### Step 5: Verify Installation
Confirm the correct Python version and packages:
```bash
python --version
pip list
```

-------------------------------------------------------------------------------------




## 4. Requirements
- Functional Requirements
    - Implement the 3 agents (Question, Response Evaluation, Validation).
    - Orchestrate them in a workflow.
    - Use shared context so agents can access stored data.
- Technical Requirements
    - Use any AI framework (e.g., LangChain, AutoGen, CrewAI, OpenAI Assistant API) and justify your choice.
    - Choose a local LLM or an external LLM API (e.g., OpenAI GPT).
    - Store context in memory or a simple database (e.g., Redis, SQLite).
    - Build a FastAPI application to expose the system as an API. Implement all routes using asynchronous programming for high performance and scalability.
    - Log each interview session with the following details
        - Candidate ID.
        - Job title/role.
        - Matching timestamp.
        - S3 URL or local file path for saved data.
        - Use DynamoDB (or SQLite/local JSON-based logs) to store the logs asynchronously.
    - Store the generated questions, responses, scores, and feedback as JSON objects in an S3 bucket (or a local equivalent, such as file storage). Use asynchronous methods for uploading files to ensure non-blocking I/O.
    - Make the code modular and easy to extend.

## Deliverables
#### Code
- A fully functional implementation of the task in your chosen framework.
- Include clear documentation on how to run the solution.
#### Short Write-Up
- Explain your approach to solving the task.
- Justify your choice of framework and key design decisions.
- Highlight any challenges you faced and how you overcame them.


-----------------------------------------------------------------------------------------------------------

## Justification of Frameworks and Design Decisions:

#### *Ollama API:* 
Chosen as the interface for interacting with the local LLM due to its simplicity and support for asynchronous communication, which is essential for scalable systems.

#### *AsyncIO:*
Allows for non-blocking operations, improving performance when handling multiple requests concurrently.

#### *Pydantic:* 
Used for schema validation to ensure that responses generated by the LLM conform to a predefined structure, enhancing reliability.

#### *LLMClient:*
Designed as a modular component to encapsulate LLM interactions, making the codebase more maintainable and extensible.

#### *Separation of Concerns:* 
Each file serves a distinct role (e.g., generating questions, evaluating responses), ensuring modularity and simplifying testing and maintenance.

#### *Reusable Agents:*
Created specific agents for question generation, response evaluation, and validation to make the system extensible for future updates.

#### *Centralized LLM Client:*
Abstracted LLM communication logic into LLMClient, making it reusable across different agents and ensuring consistent configuration.

---------------------------------------------------------------------------------------

#### *1. Challenge:* 
Understanding the System's Purpose and Role of Each Component
##### Solution: 
Reviewed the code in-depth and deduced the workflow of generating, evaluating, and validating interview responses. Analyzed key patterns and naming conventions to infer each component’s role.

#### *2. Challenge:* 
Ensuring that responses from the LLM are in the expected format.
##### Solution:
Leveraged Pydantic for schema validation, which checks the response structure and raises descriptive errors if validation fails.




