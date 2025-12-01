# SQL Chat Agent — LangChain SQL Toolkit + Agent

## Overview
This repo demonstrates an AI agent that converses with a SQL database (SQLite or MySQL), converts natural language to SQL, executes queries, and returns human-friendly answers. The UI is built with ReactJS, and the backend uses FastAPI.

Improvements:
- Added a `data/` folder with sample CSV files (employees.csv and departments.csv) to get you started. These represent a simple company database.
- You can use these samples directly or replace them with your own CSVs.
- Updated example query in UI to match sample data.
- The data comes from CSV files in the `data/` directory. You can source CSVs from anywhere (e.g., generate programmatically, download public datasets like from Kaggle, export from spreadsheets). The provided samples are for demo purposes.
- Fixed imports in agent.py for compatibility with modern LangChain (e.g., ConversationBufferMemory from langchain.memory.buffer).
- Removed Together AI to avoid compatibility issues; retained other free LLMs (Groq, OpenRouter, GitHub Models).
- Updated backend run command to use `python -m uvicorn` for Windows venv reliability.

To use free resources:
- **Groq**: Sign up at https://groq.com, get API key. Fast inference, free with rate limits.
- **OpenRouter**: Sign up at https://openrouter.ai, get API key. Use free models like llama-3.1-8b-instruct:free.
- **GitHub Models**: Generate PAT at https://github.com/settings/tokens. Free access to models.
- Other free options (not integrated but can be added): Cloudflare Workers AI, Ollama (local), AI/ML API (aimlapi.com) - modify get_llm() accordingly.

## Quick start (SQLite with sample data)
1. Create a Python venv and activate:.

## Quick start (SQLite with sample data)
1. Create a Python venv and activate:
```
python -m venv myenv
myenv\Scripts\activate  # On Windows
```

2. Install packages:
```
pip install -r requirements.txt
```

3. Add LLM keys to `.env` (focus on free ones):
```
copy .env.example .env
# Edit .env -> set GROQ_API_KEY, OPENROUTER_API_KEY, etc.
```

4. Use the provided sample data in `data/` or add your own CSVs. Then create SQLite DB:
```
python db_prep_sqlite.py
# This creates mydata.db from the CSVs
```

5. Start the FastAPI backend:
```
python -m uvicorn backend:app --reload --host 0.0.0.0 --port 8000
```

6. Start the React frontend:
```
cd frontend
npm install
npm start
```
- Open http://localhost:3000 in your browser.
- In the UI, choose DB type, set details (e.g., mydata.db for SQLite), select a free LLM provider (e.g., Groq), click `Connect to DB & Create Agent`.
- Then ask questions (e.g., "Top 5 employees by salary" or "List departments").

## MySQL
- Ensure MySQL server is running and create a database.
- Edit `.env` for MySQL credentials.
- Upload CSVs: `python db_prep_mysql.py`.
- In the React UI, select `MySQL (remote)`, fill in fields, select LLM, and connect.

## Notes & Safety
- This example uses an LLM to generate SQL. For production, enable query validation and strict least-privilege DB user.
- The agent includes a query checker for safer behavior.
- Free LLM providers have rate limits and may require sign-up. Check their docs for current models and limits.
- The backend runs on port 8000 (configurable in .env), and frontend on 3000.
- To add more free providers (e.g., Ollama): Update get_llm() in agent.py with ChatOllama(base_url="http://localhost:11434/v1").
- If using a different backend port, update `BACKEND_URL` in frontend/src/App.js.
- If you encounter import errors, ensure all packages are installed via `pip install -r requirements.txt` and restart the venv/server.