FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir \ "fastmcp==2.13.0.2" \ "mcp==1.20.0" \ "psutil==5.9.8" \ "pydantic==2.12.4" \ "python-dotenv>=1.0.1" \ "httpx>=0.27.2"

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY mcp_server.py /app/mcp_server.py

ENV DIR_WORKSPACE=/workSpace

EXPOSE 8000

CMD ["python", "/app/mcp_server.py"]