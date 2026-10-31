
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [sessionId, setSessionId] = useState("");
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function newChat() {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/new-chat`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("Unable to create a new chat");
      }

      const data = await response.json();

      setSessionId(data.session_id);
      setMessages([]);
      setInput("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function sendMessage() {
    if (!input.trim() || !sessionId || loading) return;

    const question = input.trim();

    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: question,
        }),
      });

      if (!response.ok) {
        throw new Error("Unable to generate a response");
      }

      const data = await response.json();

      setMessages((previous) => [
        ...previous,
        { role: "user", content: question },
        { role: "assistant", content: data.response },
      ]);

      setInput("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <h1>Week 3 - AI Chat with Memory</h1>

      <button onClick={newChat} disabled={loading}>
        + New Chat
      </button>

      <p>
        {sessionId
          ? `Session ID: ${sessionId}`
          : "Click New Chat to start a conversation."}
      </p>

      <div className="chat-box">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <strong>
              {message.role === "user" ? "You" : "AI"}
            </strong>

            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.content}
            </ReactMarkdown>
          </div>
        ))}

        {loading && <p>Processing...</p>}
      </div>

      {error && <p className="error">{error}</p>}

      <div className="input-area">
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(event) => setInput(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter") sendMessage();
          }}
          disabled={!sessionId || loading}
        />

        <button
          onClick={sendMessage}
          disabled={!sessionId || loading || !input.trim()}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default App;

