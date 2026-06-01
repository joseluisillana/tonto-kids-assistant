import type { ChatMessage } from "../types/conversation.js";

type ConversationPanelProps = {
  messages: ChatMessage[];
};

export function ConversationPanel({ messages }: ConversationPanelProps) {
  return (
    <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-y-auto pr-1">
      {messages.length === 0 ? (
        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-5 text-sm leading-6 text-slate-500">
          La conversacion aparecera aqui cuando envies una pregunta al backend.
        </div>
      ) : null}

      {messages.map((message) => {
        const user = message.role === "user";
        return (
          <article
            className={`max-w-[88%] rounded-3xl px-5 py-4 text-sm leading-6 shadow-sm ${
              user
                ? "ml-auto bg-coral-50 text-slate-900"
                : "mr-auto bg-sky-50 text-slate-900"
            }`}
            key={message.id}
          >
            <p>{message.text}</p>
            <time className="mt-2 block text-right text-xs text-slate-400">
              {formatTime(message.createdAt)}
            </time>
          </article>
        );
      })}
    </div>
  );
}

function formatTime(date: Date) {
  return date.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}
