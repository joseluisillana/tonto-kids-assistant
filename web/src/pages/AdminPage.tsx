import { ChatComposer } from "../components/ChatComposer.js";
import { ConversationPanel } from "../components/ConversationPanel.js";
import { MetricCard } from "../components/MetricCard.js";
import { SessionCard } from "../components/SessionCard.js";
import { VoiceLoopPanel } from "../components/VoiceLoopPanel.js";
import { TontoBot } from "../components/TontoBot.js";
import { TontoLogo } from "../components/TontoLogo.js";
import type { useConversation } from "../features/conversation/useConversation.js";

type AdminPageProps = {
  conversation: ReturnType<typeof useConversation>;
};

export function AdminPage({ conversation }: AdminPageProps) {
  const voiceBusy =
    conversation.voice.captureStatus === "requesting-permission" ||
    conversation.voice.captureStatus === "recording" ||
    conversation.voice.captureStatus === "encoding" ||
    conversation.voice.captureStatus === "uploading" ||
    conversation.voice.captureStatus === "transcribing" ||
    conversation.status === "speaking";
  const sending =
    conversation.status === "sending" ||
    conversation.status === "thinking" ||
    voiceBusy;

  return (
    <main className="min-h-screen bg-gradient-to-br from-sky-100 via-white to-coral-50 p-5 pt-24 text-slate-950">
      <div className="grid min-h-[calc(100vh-7.25rem)] gap-6 xl:grid-cols-[28rem_minmax(0,1fr)_26rem]">
        <section className="flex min-h-[38rem] flex-col rounded-[2rem] border border-white/80 bg-white/90 p-6 shadow-xl shadow-sky-200/50">
          <TontoLogo variant="light" />
          <h1 className="mt-8 text-lg font-bold text-blue-950">
            Conversacion
          </h1>
          <div className="mt-5 min-h-0 flex-1">
            <ConversationPanel messages={conversation.messages} />
          </div>
          <div className="mt-5">
            <button className="w-full rounded-2xl border border-blue-100 bg-white px-5 py-4 text-sm font-bold text-blue-600">
              Explorar temas
            </button>
          </div>
        </section>

        <section className="relative flex min-h-[38rem] flex-col items-center justify-center overflow-hidden rounded-[2rem] bg-white/35 p-6">
          <div className="absolute left-10 top-12 h-20 w-20 rounded-full bg-amber-300/80 blur-2xl" />
          <div className="absolute right-12 top-24 h-24 w-24 rounded-full bg-blue-300/60 blur-2xl" />
          <div className="mb-8 rounded-full bg-coral-400 px-8 py-4 text-lg font-black text-white shadow-xl shadow-coral-300/40">
            Sesion demo
          </div>
          <TontoBot status={conversation.status} />
          <div className="mt-8 rounded-full bg-white px-8 py-4 text-lg font-bold text-emerald-600 shadow-lg">
            {getStatusCopy(conversation.status)}
          </div>
          <div className="mt-8 w-full max-w-3xl">
            <ChatComposer
              disabled={sending}
              onSend={conversation.sendMessage}
              placeholder="Pregunta algo"
            />
          </div>
          {conversation.error ? (
            <p className="mt-4 max-w-3xl rounded-2xl bg-rose-50 px-5 py-3 text-sm font-semibold text-rose-700">
              {conversation.error}
            </p>
          ) : null}
        </section>

        <aside className="space-y-6">
          <SessionCard
            backendStatus={conversation.backendStatus}
            elapsedSeconds={conversation.elapsedSeconds}
            latestLatencyMs={conversation.latestLatencyMs}
            questionCount={conversation.questionCount}
            sessionId={conversation.sessionId}
          />

          <VoiceLoopPanel compact conversation={conversation} />

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-xl font-bold text-blue-950">Rendimiento</h2>
            <div className="mt-5 grid grid-cols-2 gap-4">
              <MetricCard
                hint="Ultima respuesta"
                label="Latencia"
                value={
                  conversation.latestLatencyMs === null
                    ? "--"
                    : `${conversation.latestLatencyMs} ms`
                }
              />
              <MetricCard
                hint="Health check"
                label="Servicio"
                value={
                  conversation.backendStatus === "connected"
                    ? "Online"
                    : "Offline"
                }
              />
            </div>
            <button
              className="mt-5 w-full rounded-2xl border border-slate-200 bg-slate-50 px-5 py-4 text-sm font-bold text-blue-600"
              onClick={() => void conversation.checkHealth()}
              type="button"
            >
              Comprobar backend
            </button>
          </section>

          <section className="rounded-3xl border border-amber-200 bg-amber-50 p-6 shadow-sm">
            <h2 className="text-xl font-bold text-blue-950">
              Consejos para ti
            </h2>
            <p className="mt-4 text-sm leading-6 text-slate-700">
              Haz preguntas cortas y educativas para validar rapido el contrato
              `/chat` antes de pasar a la Raspberry.
            </p>
          </section>

          <button
            className="w-full rounded-3xl border border-blue-100 bg-white px-5 py-5 text-sm font-bold text-blue-600 shadow-sm"
            onClick={conversation.resetSession}
            type="button"
          >
            Reiniciar sesion
          </button>
        </aside>
      </div>
    </main>
  );
}

function getStatusCopy(status: ReturnType<typeof useConversation>["status"]) {
  if (status === "thinking") {
    return "Estoy pensando...";
  }
  if (status === "speaking") {
    return "Respuesta lista";
  }
  if (status === "error") {
    return "Necesito ayuda tecnica";
  }
  if (status === "listening") {
    return "Escuchando";
  }

  return "Listo para hablar";
}
