# agent.py
"""
Initialize an agent that can query a SQL database using LangChain's SQL toolkit.
Provides a function `create_agent_for_uri(uri)` that returns an agent executor.
"""

import os
from typing import Optional
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain.memory.buffer import ConversationBufferMemory
import config

def get_llm(llm_provider: str = "openai"):
    """
    Create and return a chat model based on the provider (swap for free alternatives).
    """
    if llm_provider == "openai":
        os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY", "")
        return ChatOpenAI(model="gpt-4o-mini", temperature=0)
    elif llm_provider == "groq":
        return ChatGroq(model="llama-3.1-70b-versatile", api_key=config.GROQ_API_KEY, temperature=0)
    elif llm_provider == "openrouter":
        # Use a free model like meta-llama/llama-3.1-8b-instruct:free
        return ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=config.OPENROUTER_API_KEY,
            model="meta-llama/llama-3.1-8b-instruct:free",
            temperature=0
        )
    elif llm_provider == "github":
        # GitHub Models
        return ChatOpenAI(
            base_url="https://models.github.ai/inference/v1",
            api_key=config.GITHUB_PAT,
            model="meta-llama/llama-3.1-8b-instruct",
            temperature=0
        )
    else:
        raise ValueError(f"Unknown LLM provider: {llm_provider}")

def create_agent_for_uri(db_uri: str, llm_provider: str = "openai", verbose: bool = False):
    """
    Build an agent bound to a SQLDatabase at `db_uri` using the specified LLM provider.
    Returns: agent_executor (callable .invoke({"input": question})["output"])
    """

    # 1) create SQLDatabase wrapper (introspects tables)
    sql_db = SQLDatabase.from_uri(db_uri)

    # 2) create LLM
    llm = get_llm(llm_provider)

    # 3) create memory for conversational behavior
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # 4) initialize agent
    agent_executor = create_sql_agent(
        llm=llm,
        db=sql_db,
        verbose=verbose,
        agent_type="zero-shot-react-description",
        agent_executor_kwargs={"memory": memory, "handle_parsing_errors": True}
    )

    return agent_executor

# Simple helper to build common URIs
def sqlite_uri(db_path: str = "mydata.db"):
    return f"sqlite:///{db_path}"

def mysql_uri(host=config.MYSQL_HOST, port=config.MYSQL_PORT, user=config.MYSQL_USER, pw=config.MYSQL_PASSWORD, db=config.MYSQL_DB):
    return f"mysql+pymysql://{user}:{pw}@{host}:{port}/{db}"

# Example usage:
if __name__ == "__main__":
    uri = sqlite_uri("mydata.db")
    agent = create_agent_for_uri(uri, llm_provider="groq", verbose=True)
    print(agent.invoke({"input": "Show me the list of tables and describe columns."})["output"])