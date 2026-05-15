import { FormEvent, useState } from "react";

type ChatComposerProps = {
  disabled?: boolean;
  onSend: (message: string) => void;
  placeholder?: string;
  tone?: "light" | "dark";
};

export function ChatComposer({
  disabled = false,
  onSend,
  placeholder = "Pregunta algo",
  tone = "light",
}: ChatComposerProps) {
  const [message, setMessage] = useState("");

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const text = message.trim();
    if (!text) {
      return;
    }

    onSend(text);
    setMessage("");
  }

  const dark = tone === "dark";

  return (
    <form
      className={`flex w-full items-center gap-3 rounded-full border p-2 shadow-xl ${
        dark
          ? "border-white/15 bg-white/10 shadow-slate-950/40"
          : "border-slate-200 bg-white shadow-slate-200/70"
      }`}
      onSubmit={handleSubmit}
    >
      <input
        className={`min-w-0 flex-1 bg-transparent px-5 py-3 text-base outline-none ${
          dark
            ? "text-white placeholder:text-slate-400"
            : "text-slate-900 placeholder:text-slate-400"
        }`}
        disabled={disabled}
        onChange={(event) => setMessage(event.target.value)}
        placeholder={placeholder}
        value={message}
      />
      <button
        className="shrink-0 rounded-full bg-blue-500 px-6 py-3 text-sm font-bold text-white shadow-lg shadow-blue-500/30 transition hover:bg-blue-600 disabled:cursor-not-allowed disabled:opacity-50"
        disabled={disabled || !message.trim()}
        type="submit"
      >
        Enviar
      </button>
    </form>
  );
}
