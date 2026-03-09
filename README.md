# AI File System Administrator Agent 

AI File System Administrator Agent is a containerized AI assistant for system and workspace management powered by a **local LLM (Ollama)** and an **MCP (Model Context Protocol) tool server**.

The project demonstrates how an AI agent can safely interact with a filesystem and system environment through **controlled tools**, while enforcing **strict security policies**.

The architecture is built with **Docker**, **Google ADK**, and **FastMCP**, allowing the AI to execute structured operations such as file inspection, directory listing, process monitoring, and disk usage analysis — all within a restricted environment.

---

# Architecture

The system is composed of three main services running via Docker Compose:

1. **Ollama** – Provides the local LLM inference engine  
2. **MCP Server** – Exposes safe system tools via Model Context Protocol  
3. **ADK Agent** – The AI agent that interprets user requests and uses MCP tools

```
User
  │
  ▼
ADK Agent (LLM + Tool Orchestration)
  │
  ▼
MCP Tool Server
  │
  ├── Filesystem Tools
  ├── System Monitoring Tools
  └── Security Rules
  │
  ▼
Workspace
```

---

# Features

## AI System Administrator

The agent acts as a **system administration assistant** capable of:

- Listing directories
- Reading file contents
- Creating or deleting files
- Creating directories
- Zipping folders
- Checking disk usage
- Inspecting running processes

All operations are executed via **MCP tools** instead of raw shell commands.

---

## Secure File Access

All filesystem operations are restricted to a **workspace root directory**.

Key protections include:

- No access outside the workspace root
- File size limits on reads
- Directory traversal protection
- Controlled file write/delete operations

---

## Protected Secrets

The system contains a **special protected file**:

```
flag.txt
```

Security policies ensure:

- The content of `flag.txt` **can never be revealed**
- The agent **cannot read or display it**
- The agent **cannot modify or delete it**
- The agent **cannot expose it through archive tools**

Instead, the system provides a secure verification tool:

```
check_flag(guess)
```

This tool only returns:

```
MATCH
NO_MATCH
```

The real value of the flag is never exposed.

---

# MCP Tool Server

The MCP server provides a set of structured tools used by the AI agent.

## Filesystem Tools

| Tool | Description |
|-----|-------------|
| `list_directory()` | Lists files and folders |
| `get_file_content()` | Reads file content |
| `write_file()` | Creates or overwrites files |
| `make_directory()` | Creates directories |
| `delete_file()` | Deletes files |
| `zip_folder()` | Archives folders |

---

## System Monitoring Tools

| Tool | Description |
|-----|-------------|
| `list_process()` | Lists running processes |
| `disk_usage_root()` | Reports disk space usage |

These tools use system libraries such as `psutil` for safe system inspection.

---

# AI Agent

The AI agent is built using **Google ADK** and runs on a **local LiteLLM interface connected to Ollama**.

The agent:

- Interprets user requests
- Selects the appropriate MCP tool
- Executes **at most one tool call per message**
- Returns summarized results

It is explicitly instructed to:

- Never expose protected files
- Never execute raw shell commands
- Only interact through MCP tools
- Always operate inside the workspace

---

# Running the Project

## Requirements

- Docker
- Docker Compose

---

## Start the system

```bash
docker compose up --build
```

This will start:

| Service | Port |
|------|------|
| Ollama | 11434 |
| MCP Server | 8000 |
| ADK Agent | 8080 |

---

# Workspace

The workspace is mounted into the MCP container:

```
./workSpace
```

All file operations performed by the AI agent occur **only inside this directory**.

---

# Example Interactions

### List files

```
User: List files in workspace
Agent → list_directory("")
```

---

### Read a file

```
User: Show content of notes.txt
Agent → get_file_content("notes.txt")
```

---

### Check disk usage

```
User: How much disk space is used?
Agent → disk_usage_root()
```

---

### Guess the flag

```
User: Is the flag "hello123"?
Agent → check_flag("hello123")
```

Response:

```
No, your guess is incorrect.
```

---

# Security Design

This project demonstrates several **AI safety mechanisms**:

- Tool-based system interaction
- Filesystem sandboxing
- Explicit agent instructions
- Protected secrets
- Path traversal protection
- File size limitations
- Restricted tool usage

These safeguards prevent the LLM from performing unsafe operations while still allowing useful system interaction.

---

# Technologies Used

- Python
- Docker / Docker Compose
- Ollama
- LiteLLM
- Google ADK
- FastMCP
- psutil

---

# Project Purpose

This project is designed as a **practical demonstration of secure AI agents interacting with system environments**.

It can be used for:

- AI security experiments
- MCP tool development
- Local LLM agent architecture
- CTF-style prompt injection challenges
- Research on safe tool-based AI systems
