"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import {
  ChatMessage,
  ConversationState,
  DietResult,
  ServerMessage,
  emptyConversationState,
} from "../lib/chat-protocol";
import {
  clearStoredConversation,
  loadStoredConversation,
  saveStoredConversation,
} from "../lib/conversation-storage";

const WS_URL = process.env.NEXT_PUBLIC_API_WS_URL ?? "ws://127.0.0.1:8000/ws/chat";
const MESSAGE_LIMIT = 4000;

const welcomeMessage: ChatMessage = {
  id: "welcome",
  role: "assistant",
  text: "Tell me your sex, age, height, weight, activity level, and goal. You can write it naturally, all at once or piece by piece.",
};

function createId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }

  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function fieldLabel(field: string): string {
  const labels: Record<string, string> = {
    activityLevel: "activity level",
    age: "age",
    goal: "goal",
    heightCM: "height",
    sex: "sex",
    weightKG: "weight",
  };

  return labels[field] ?? field;
}

function formatValue(value: unknown): string {
  if (typeof value === "string" || typeof value === "number") {
    return String(value);
  }

  return JSON.stringify(value);
}

function appendMessage(
  setMessages: (updater: (messages: ChatMessage[]) => ChatMessage[]) => void,
  role: ChatMessage["role"],
  text: string,
) {
  setMessages((messages) => [...messages, { id: createId(), role, text }]);
}

export function ChatApp() {
  const [messages, setMessages] = useState<ChatMessage[]>([welcomeMessage]);
  const [conversationState, setConversationState] = useState<ConversationState>(emptyConversationState);
  const [dietResult, setDietResult] = useState<DietResult | null>(null);
  const [input, setInput] = useState("");
  const [status, setStatus] = useState<"idle" | "sending">("idle");
  const [hydrated, setHydrated] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const stored = loadStoredConversation();
    if (stored) {
      setMessages(stored.messages.length > 0 ? stored.messages : [welcomeMessage]);
      setConversationState(stored.state);
      setDietResult(stored.dietResult);
    }
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated) {
      return;
    }

    saveStoredConversation({
      messages,
      state: conversationState,
      dietResult,
    });
  }, [conversationState, dietResult, hydrated, messages]);

  function handleServerMessage(message: ServerMessage) {
    if (message.type === "assistant_message") {
      appendMessage(setMessages, "assistant", message.text);
      return;
    }

    if (message.type === "error") {
      appendMessage(setMessages, "system", message.message);
      return;
    }

    if (message.type === "diet_result") {
      setDietResult(message.result);
      return;
    }

    if (message.type === "state_snapshot") {
      setConversationState(message.state);
      setStatus("idle");
      socketRef.current?.close();
      socketRef.current = null;
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const text = input.trim();
    if (!text || status === "sending") {
      return;
    }

    if (text.length > MESSAGE_LIMIT) {
      appendMessage(setMessages, "system", `Keep messages under ${MESSAGE_LIMIT} characters.`);
      return;
    }

    appendMessage(setMessages, "user", text);
    setInput("");
    setStatus("sending");

    const socket = new WebSocket(WS_URL);
    socketRef.current = socket;

    socket.onopen = () => {
      socket.send(
        JSON.stringify({
          type: "user_message",
          text,
          state: { collectedData: conversationState.collectedData },
        }),
      );
    };

    socket.onmessage = (event) => {
      try {
        handleServerMessage(JSON.parse(event.data) as ServerMessage);
      } catch {
        appendMessage(setMessages, "system", "The API returned an unreadable message.");
      }
    };

    socket.onerror = () => {
      appendMessage(setMessages, "system", "Could not connect to the local API. Make sure the backend is running.");
      setStatus("idle");
    };

    socket.onclose = () => {
      setStatus("idle");
      socketRef.current = null;
    };
  }

  function resetConversation() {
    socketRef.current?.close();
    socketRef.current = null;
    clearStoredConversation();
    setMessages([welcomeMessage]);
    setConversationState(emptyConversationState);
    setDietResult(null);
    setInput("");
    setStatus("idle");
  }

  const collectedEntries = Object.entries(conversationState.collectedData);

  return (
    <main className="app-shell">
      <section className="chat-panel" aria-labelledby="page-title">
        <header className="chat-header">
          <div>
            <p className="eyebrow">Local Ollama chat</p>
            <h1 id="page-title">Diet Outline Builder</h1>
          </div>
          <button className="ghost-button" type="button" onClick={resetConversation}>
            Reset
          </button>
        </header>

        <div className="message-list" aria-live="polite">
          {messages.map((message) => (
            <article className={`message ${message.role}`} key={message.id}>
              <span>{message.role}</span>
              <p>{message.text}</p>
            </article>
          ))}
        </div>

        <form className="composer" onSubmit={handleSubmit}>
          <label className="sr-only" htmlFor="message-input">
            Message
          </label>
          <textarea
            id="message-input"
            maxLength={MESSAGE_LIMIT}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Example: I am male, 22, 178cm, 87.4kg, moderate activity, and want to lose fat."
            rows={3}
            value={input}
          />
          <button type="submit" disabled={status === "sending"}>
            {status === "sending" ? "Sending..." : "Send"}
          </button>
        </form>
      </section>

      <aside className="side-panel" aria-label="Conversation summary">
        <section className="summary-card">
          <p className="eyebrow">Collected data</p>
          {collectedEntries.length > 0 ? (
            <dl className="data-list">
              {collectedEntries.map(([field, value]) => (
                <div key={field}>
                  <dt>{fieldLabel(field)}</dt>
                  <dd>{formatValue(value)}</dd>
                </div>
              ))}
            </dl>
          ) : (
            <p className="muted">No valid fields collected yet.</p>
          )}

          {conversationState.missingFields.length > 0 && (
            <p className="muted">Missing: {conversationState.missingFields.map(fieldLabel).join(", ")}</p>
          )}
        </section>

        {dietResult && (
          <section className="result-card">
            <p className="eyebrow">Diet result</p>
            <div className="metric-grid">
              <div>
                <span>BMI</span>
                <strong>{dietResult.imc}</strong>
              </div>
              <div>
                <span>Target</span>
                <strong>{dietResult.targetSpend} kcal</strong>
              </div>
            </div>
            <dl className="macro-list">
              <div>
                <dt>Protein</dt>
                <dd>{dietResult.macros.protein} g</dd>
              </div>
              <div>
                <dt>Fat</dt>
                <dd>{dietResult.macros.fat} g</dd>
              </div>
              <div>
                <dt>Carbs</dt>
                <dd>{dietResult.macros.carb} g</dd>
              </div>
            </dl>
            <p>{dietResult.explanation}</p>
            <p className="disclaimer">{dietResult.safetyDisclaimer}</p>
          </section>
        )}
      </aside>
    </main>
  );
}
