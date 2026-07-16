import { useState, useRef, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./App.css";

const suggestions = [
  "What can you do?",
  "Explain OSPF",
  "Configure VLAN 10",
  "Why can't I ping another subnet?",
  "Troubleshoot DHCP",
  "Show NAT configuration"
];

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const sendQuestion = async (text) => {
    if (!text.trim() || loading) return;

    const userMessage = {
      sender: "user",
      text,
      time: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };

    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
          message: text,
        }
      );

      const botMessage = {
        sender: "bot",
        text: response.data.response,
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text:
            "❌ Unable to connect to the backend.\n\nPlease make sure FastAPI is running.",
          time: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        },
      ]);
    }

    setLoading(false);
    setQuestion("");
  };

  const askQuestion = () => {
    sendQuestion(question);
  };

  const clearChat = () => {
    setMessages([]);
    setQuestion("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      askQuestion();
    }
  };

  return (
    <div className="app">

      {/* Sidebar */}

      <aside className="sidebar">

        <h2>🌐 Cisco AI</h2>

        <button
          className="new-chat-btn"
          onClick={clearChat}
        >
          + New Chat
        </button>

        <div className="sidebar-section">

          <h3>Suggested Topics</h3>

          {suggestions.map((item, index) => (
            <button
              key={index}
              className="suggestion-btn"
              onClick={() => sendQuestion(item)}
            >
              {item}
            </button>
          ))}

        </div>

      </aside>

      {/* Main Area */}

      <main className="main-content">

        <header className="header">

          <div>

            <h1>
               Network Troubleshooting Assistant
            </h1>

            <p>
              Powered by Llama 3.2 + Retrieval-Augmented Generation
            </p>

          </div>

        </header>

        <div className="chat-window">

          {messages.length === 0 && (

            <div className="welcome">

              <h2>👋 Welcome!</h2>

              <p>
                Ask me anything about Cisco networking,
                routing, switching, VLANs, OSPF,
                DHCP, NAT, ACLs, VPNs and more.
              </p>

              <div className="welcome-grid">

                {suggestions.map((item, index) => (

                  <div
                    key={index}
                    className="welcome-card"
                    onClick={() => sendQuestion(item)}
                  >

                    {item}

                  </div>

                ))}

              </div>

            </div>

          )}

          {messages.map((msg, index) => (

            <div
              key={index}
              className={
                msg.sender === "user"
                  ? "message user"
                  : "message bot"
              }
            >

              <div className="avatar">
                {msg.sender === "user" ? "👤" : "🤖"}
              </div>

              <div className="bubble">

                <div className="message-header">

                  <strong>
                    {msg.sender === "user"
                      ? "You"
                      : "Assistant"}
                  </strong>

                  <span>{msg.time}</span>

                </div>

                <ReactMarkdown>

                  {msg.text}

                </ReactMarkdown>

              </div>

            </div>

          ))}

          {loading && (

            <div className="message bot">

              <div className="avatar">
                🤖
              </div>

              <div className="bubble">

                <div className="message-header">

                  <strong>Assistant</strong>

                </div>

                <div className="typing">

                  <span></span>
                  <span></span>
                  <span></span>

                </div>

                <p className="typing-text">
                  Searching Cisco documentation...
                </p>

              </div>

            </div>

          )}

          <div ref={chatEndRef}></div>

        </div>
        <div className="input-area">

          <textarea
            rows="3"
            placeholder="Ask a networking question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
          />

          <button
            className="send-btn"
            onClick={askQuestion}
            disabled={loading}
          >
            {loading ? "..." : "➤"}
          </button>

        </div>

      </main>

    </div>
  );
}

export default App;