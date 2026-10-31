
import { useState } from "react";
import ReactMarkdown from "react-markdown";

function App() {

  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [intent, setIntent] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const generateResponse = async () => {

    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setError("");
    setResponse("");
    setIntent("");

    try {

      const result = await fetch(
        "http://localhost:8000/generate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            question: question
          })
        }
      );

      if (!result.ok) {
        throw new Error("Failed to generate response");
      }

      const data = await result.json();

      setIntent(data.intent);
      setResponse(data.response);

    } catch (err) {

      setError(
        "Something went wrong. Please try again."
      );

    } finally {

      setLoading(false);

    }
  };

  return (
    <div style={{
      padding: "30px",
      maxWidth: "850px",
      margin: "auto"
    }}>

      <h1>Week 2 - AI Response Generator</h1>

      <h3>Enter your question</h3>

      <textarea
        rows="5"
        style={{ width: "100%", padding: "10px" }}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask anything..."
      />

      <br /><br />

      <button
        onClick={generateResponse}
        disabled={loading}
      >
        {loading ? "Generating..." : "Generate Response"}
      </button>

      <hr />

      {error && (
        <p style={{ color: "red" }}>{error}</p>
      )}

      {intent && (
        <p>
          <strong>Detected Intent:</strong> {intent}
        </p>
      )}

      <ReactMarkdown>{response}</ReactMarkdown>

    </div>
  );
}

export default App;


