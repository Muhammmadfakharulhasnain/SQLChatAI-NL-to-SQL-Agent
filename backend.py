# backend.py
"""
FastAPI backend to serve the SQL agent.
Run with: python -m uvicorn backend:app --reload --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agent import create_agent_for_uri

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent_executor = None

@app.post("/connect")
def connect(body: dict = Body(...)):
    db_uri = body.get("db_uri")
    llm_provider = body.get("llm_provider", "openai")
    if not db_uri:
        raise HTTPException(status_code=400, detail="db_uri is required")
    global agent_executor
    try:
        agent_executor = create_agent_for_uri(db_uri, llm_provider=llm_provider, verbose=False)
        return {"status": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def query(question: str = Body(..., embed=True)):
    global agent_executor
    if agent_executor is None:
        raise HTTPException(status_code=400, detail="Agent not connected")
    try:
        result = agent_executor.invoke({"input": question})["output"]
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))