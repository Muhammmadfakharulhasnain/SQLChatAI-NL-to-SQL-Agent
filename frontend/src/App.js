import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const BACKEND_URL = 'http://localhost:8000';

function App() {
  const [dbType, setDbType] = useState('SQLite');
  const [dbPath, setDbPath] = useState('mydata.db');
  const [mysqlHost, setMysqlHost] = useState('127.0.0.1');
  const [mysqlPort, setMysqlPort] = useState(3306);
  const [mysqlUser, setMysqlUser] = useState('root');
  const [mysqlPwd, setMysqlPwd] = useState('');
  const [mysqlDb, setMysqlDb] = useState('company_db');
  const [llmProvider, setLlmProvider] = useState('groq'); // Default to free Groq
  const [connected, setConnected] = useState(false);
  const [question, setQuestion] = useState('');
  const [history, setHistory] = useState([]);

  const handleConnect = async () => {
    let uri = '';
    if (dbType === 'SQLite') {
      uri = `sqlite:///${dbPath}`;
    } else {
      uri = `mysql+pymysql://${mysqlUser}:${mysqlPwd}@${mysqlHost}:${mysqlPort}/${mysqlDb}`;
    }
    try {
      await axios.post(`${BACKEND_URL}/connect`, { db_uri: uri, llm_provider: llmProvider });
      setConnected(true);
      setHistory([]); // Reset history on new connection
    } catch (e) {
      alert(`Failed to connect: ${e.response ? e.response.data.detail : e.message}`);
    }
  };

  const handleSend = async () => {
    if (!question.trim()) {
      alert('Enter a question.');
      return;
    }
    try {
      const res = await axios.post(`${BACKEND_URL}/query`, { question });
      const answer = res.data.answer;
      setHistory([...history, { question, answer }]);
      setQuestion('');
    } catch (e) {
      alert(`Error: ${e.response ? e.response.data.detail : e.message}`);
    }
  };

  return (
    <div className="app-container">
      <h1 className="app-header">🗄️ SQL Chat Agent — LangChain + SQLToolkit</h1>
      <div className="config">
        <h2>Database Configuration</h2>
        <div className="form-row">
          <select value={dbType} onChange={(e) => setDbType(e.target.value)} className="select">
            <option>SQLite (local)</option>
            <option>MySQL (remote)</option>
          </select>
        </div>
        {dbType === 'SQLite' ? (
          <div>
            <input
              type="text"
              value={dbPath}
              onChange={(e) => setDbPath(e.target.value)}
              placeholder="SQLite DB path"
              className="input"
            />
          </div>
        ) : (
          <div>
            <div className="form-row">
              <input
                type="text"
                value={mysqlHost}
                onChange={(e) => setMysqlHost(e.target.value)}
                placeholder="MySQL Host"
                className="input"
              />
              <input
                type="number"
                value={mysqlPort}
                onChange={(e) => setMysqlPort(e.target.value)}
                placeholder="MySQL Port"
                className="input"
              />
            </div>
            <div className="form-row">
              <input
                type="text"
                value={mysqlUser}
                onChange={(e) => setMysqlUser(e.target.value)}
                placeholder="MySQL User"
                className="input"
              />
              <input
                type="password"
                value={mysqlPwd}
                onChange={(e) => setMysqlPwd(e.target.value)}
                placeholder="MySQL Password"
                className="input"
              />
            </div>
            <input
              type="text"
              value={mysqlDb}
              onChange={(e) => setMysqlDb(e.target.value)}
              placeholder="MySQL Database"
              className="input"
            />
          </div>
        )}
        <h2 className="label">LLM Provider (Free Options Preferred)</h2>
        <select value={llmProvider} onChange={(e) => setLlmProvider(e.target.value)} className="select">
          <option value="openai">OpenAI (Paid)</option>
          <option value="groq">Groq (Free)</option>
          <option value="openrouter">OpenRouter (Free Tier)</option>
          <option value="github">GitHub Models (Free)</option>
        </select>
        <div style={{ height: 12 }} />
        <button onClick={handleConnect} className="btn">Connect to DB & Create Agent</button>
      </div>
      {connected && (
        <div>
          <h2>Chat with your database</h2>
          <div className="chat-input">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a question (e.g., 'Top 5 employees by salary')"
              className="input"
            />
            <button onClick={handleSend} className="btn">Send</button>
          </div>
          <div style={{ marginTop: '20px' }}>
            {history.slice().reverse().map((item, idx) => (
              <div key={idx} className="chat-message">
                <strong>Q:</strong> {item.question}
                <br />
                <strong>A:</strong> {item.answer}
              </div>
            ))}
          </div>
        </div>
      )}
      {!connected && <p>Create/connect the agent first.</p>}
    </div>
  );
}

export default App;