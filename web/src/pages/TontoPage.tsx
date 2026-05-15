import { ActivityTimeline } from "../components/ActivityTimeline";
import { ChatComposer } from "../components/ChatComposer";
import { StatusPill } from "../components/StatusPill";
import { TontoBot } from "../components/TontoBot";
import { TontoLogo } from "../components/TontoLogo";
import type { useConversation } from "../features/conversation/useConversation";

type TontoPageProps = {
  conversation: ReturnType<typeof useConversation>;
};

export function TontoPage({ conversation }: TontoPageProps) {
  const lastAssistantMessage = [...conversation.messages]
    .reverse()
    .find((message) => message.role === "assistant");
  const lastUserMessage = [...conversation.messages]
    .reverse()
    .find((message) => message.role === "user");
  const sending =
    conversation.status === "sending" || conversation.status === "thinking";

  return (
    <main className="min-h-screen bg-slate-950 p-5 pt-24 text-white">
      <div className="mx-auto grid min-h-[calc(100vh-7.25rem)] max-w-[100rem] gap-5 xl:grid-cols-[minmax(0,1fr)_25rem]">
        <section className="relative overflow-hidden rounded-[2rem] bg-gradient-to-br from-slate-900 via-slate-950 to-blue-950 p-7 shadow-2xl shadow-black/40">
          <div className="absolute inset-x-0 top-0 h-48 bg-mint-200/10" />
          <div className="relative z-10 flex flex-wrap items-center justify-between gap-4">
            <TontoLogo />
            <StatusPill status={conversation.backendStatus} />
          </div>

          <div className="relative z-10 mt-10 grid items-center gap-8 lg:grid-cols-[22rem_minmax(0,1fr)]">
            <TontoBot status={conversation.status} />

            <div className="rounded-[2rem] bg-white p-6 text-slate-950 shadow-2xl shadow-black/20">
              <div className="mb-5 inline-flex rounded-full bg-mint-100 px-5 py-3 text-lg font-black text-blue-950">
                {getStatusCopy(conversation.status)}
              </div>
              <h1 className="text-4xl font-black tracking-normal text-blue-950">
                {lastUserMessage?.text ?? "Haz una pregunta a TONTO"}
              </h1>
              <div className="mt-6 rounded-3xl bg-slate-100 p-6 text-xl leading-9 text-blue-950">
                {lastAssistantMessage?.text ??
                  "Usa el panel inferior para probar el mismo flujo que usa la Raspberry Pi."}
              </div>
              {conversation.error ? (
                <p className="mt-4 rounded-2xl bg-rose-50 px-5 py-3 text-sm font-semibold text-rose-700">
                  {conversation.error}
                </p>
              ) : null}
            </div>
          </div>

          <div className="relative z-10 mt-8">
            <ChatComposer
              disabled={sending}
              onSend={conversation.sendMessage}
              placeholder="Escribe una pregunta para TONTO"
              tone="dark"
            />
          </div>

          <div className="relative z-10 mt-7 grid gap-4 md:grid-cols-4">
            <ActionButton
              label="Escuchar"
              onClick={() => conversation.setStatus("listening")}
              tone="mint"
            />
            <ActionButton
              label="Hablar"
              onClick={() => conversation.setStatus("listening")}
              tone="coral"
            />
            <ActionButton
              label="Repetir"
              onClick={conversation.repeatLatest}
              tone="purple"
            />
            <ActionButton
              label="Parar"
              onClick={() => conversation.setStatus("idle")}
              tone="navy"
            />
          </div>
        </section>

        <aside className="rounded-[2rem] bg-blue-950 p-6 shadow-2xl shadow-black/30">
          <h2 className="text-2xl font-black text-mint-200">Actividad</h2>
          <div className="mt-7">
            <ActivityTimeline events={conversation.activity} />
          </div>
          <div className="mt-8 rounded-3xl border border-white/15 bg-white/8 p-5">
            <p className="text-sm font-bold text-mint-200">Sesion activa</p>
            <p className="mt-2 break-all text-sm text-white/90">
              {conversation.sessionId}
            </p>
            <p className="mt-4 text-sm text-white/70">
              Preguntas: {conversation.questionCount}
            </p>
          </div>
        </aside>
      </div>
    </main>
  );
}

function ActionButton({
  label,
  onClick,
  tone,
}: {
  label: string;
  onClick: () => void;
  tone: "mint" | "coral" | "purple" | "navy";
}) {
  const toneClass = {
    mint: "bg-mint-300 text-blue-950 shadow-mint-300/30",
    coral: "bg-coral-400 text-white shadow-coral-400/30",
    purple: "bg-purple-500 text-white shadow-purple-500/30",
    navy: "bg-slate-800 text-white shadow-black/30",
  }[tone];

  return (
    <button
      className={`min-h-24 rounded-3xl px-5 py-5 text-xl font-black shadow-xl transition hover:-translate-y-0.5 ${toneClass}`}
      onClick={onClick}
      type="button"
    >
      {label}
    </button>
  );
}

function getStatusCopy(status: ReturnType<typeof useConversation>["status"]) {
  if (status === "thinking") {
    return "Pensando";
  }
  if (status === "speaking") {
    return "Respuesta enviada";
  }
  if (status === "error") {
    return "Error";
  }
  if (status === "listening") {
    return "Escuchando";
  }

  return "Listo";
}
