# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
# Copy requirements file first to leverage Docker cache
COPY interviewer/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY interviewer/ ./

# Expose the application port
EXPOSE 8765

# Set the entry point for the application
CMD ["python", "main.py"]


#FROM python:3.13-slim
#
#WORKDIR /app
#COPY . /app
#RUN pip install -r requirements.txt
#
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8765"]
