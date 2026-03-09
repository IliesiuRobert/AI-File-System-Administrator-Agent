FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir \ "google-adk==1.18.0" \ "litellm==1.79.1" \ "openai>=1.46.0" \ "httpx>=0.27.2" \ "python-dotenv>=1.0.1"

RUN mkdir -p /app/agents/my_agent

COPY .env       /app/agents/my_agent/.env
COPY __init__.py /app/agents/my_agent/__init__.py
COPY agent.py    /app/agents/my_agent/agent.py

EXPOSE 8080
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8080", "/app/agents"]