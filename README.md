# AgentScore — Student Score Lookup Agent

A small Python-based assistant that logs into a university API and retrieves a student's grades. It uses a conversational LLM (via langchain_google_genai) with a single tool to fetch score data. The assistant is configured to always call the tool when the user asks about grades and to return exactly one single-line answer.

---

## Features

- Authenticate to the university gateway and obtain an access token.
- Query the student information endpoint to get the student ID.
- Request the student's grade report and return answers via an LLM agent.
- Strict reply format enforced by the agent's system prompt (single-line answers, no hallucination).

---

## Repository layout

- `agentscore.py` — Main program. Starts the LLM agent, registers the `get_scores_tool`, and enters an interactive loop.
- `login.py` — Performs authentication and returns an access token.
- `getstudent_id.py` — Calls the API to obtain the student's internal ID.
- `getscore.py` — Requests the student's grades (result JSON) using the access token and student ID.
- `requirements.txt` — Python dependencies used by the project.

---

## Prerequisites

- Python 3.8+ (project was developed with Python 3.11; use 3.11 if possible).
- A working internet connection to reach the university APIs and the Google generative APIs.
- Credentials / API keys required by `langchain_google_genai` and any service it depends on. The project calls `dotenv.load_dotenv()` so you can store secrets in a `.env` file.

Note: This project performs real requests to external endpoints (university APIs). Make sure you have permission to access them and you protect any account credentials.

---

## Setup (Windows PowerShell)

1. Create and activate a virtual environment:

    python -m venv venv
    .\venv\Scripts\Activate

2. Install dependencies:

    pip install -r requirements.txt

3. Provide environment configuration:

- Create a `.env` file in the project root (or set environment variables via PowerShell). The project uses `dotenv` but doesn't hardcode variable names for the LLM provider; add whatever keys your `langchain_google_genai` integration requires (for example `GOOGLE_API_KEY` or credentials file path). Example `.env` content:

    # .env
    # Set provider-specific credentials required by your LLM integration
    GOOGLE_API_KEY=your_api_key_here

Alternatively, set env vars in PowerShell for a single session:

    $env:GOOGLE_API_KEY = "your_api_key_here"

4. Run the agent:

    python agentscore.py

You will be prompted for your university username and password at startup.

---

## Usage

- After launching, the program asks for `Username:` and `Password:`. Provide your university credentials.
- In the interactive prompt, ask about grades. Examples:
  - "Điểm môn Toán?" (Vietnamese)
  - "What is my grade for [course name]?"
  - "Show my scores"
- To exit: type `exit` or `quit`.

Behavior notes:
- The agent is instructed to always call the `get_scores_tool` when the user asks about scores. The tool returns the JSON result from the university API; the LLM formats a single-line reply based on that data.
- Reply formatting rules are strict — the agent returns exactly one line. If the LLM can't find the requested course it will reply with the "not found" template.

---

## Security and privacy

- Credentials and tokens are sensitive. Do not commit `.env` or other secrets to version control. Add `.env` to `.gitignore` if needed.
- The program uses external APIs; be mindful of rate limits and terms of service.

---

## Troubleshooting

- `requests.exceptions.HTTPError` — check that the username/password are correct and that the API endpoints are reachable.
- Authentication fails — verify the `login` function payload matches the university's expected format and that the gateway URL (`login_url`) is correct.
- LLM errors — confirm your Google/LLM credentials are set and that `langchain_google_genai` is correctly installed and configured.
- If the program raises JSON/key errors when parsing responses, inspect the raw responses returned by the API endpoints to ensure the expected fields exist.

---

## Next steps / Improvements

- Add unit tests for the three API wrapper modules (`login.py`, `getstudent_id.py`, `getscore.py`) using mocked HTTP responses.
- Add more robust token refresh/error handling and better secrets management (e.g., use a secrets manager).
- Add a non-interactive CLI mode that accepts username/password via environment variables or secure input for automation.
- Limit the scope of the LLM's tool access and add logging/auditing for tool calls.

---

## License

This repository has no explicit license file. If you intend to share or distribute this project, add a LICENSE file describing the terms.

---

If you'd like, I can also:
- Add a sample `.env.example` file,
- Create basic unit tests for the API wrappers,
- Or convert the interactive prompt into a small CLI with flags for username/password and output formatting.

Tell me which of those you'd like next and I will implement it.
