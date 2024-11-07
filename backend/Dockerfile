FROM python:3.11-slim

WORKDIR /code

# Copy requirements first for better caching
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./db /code/db
COPY ./agents /code/agents
COPY ./main.py /code/main.py


# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
