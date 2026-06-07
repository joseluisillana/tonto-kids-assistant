import { ActivityTimeline } from "../components/ActivityTimeline.js";
import { ChatComposer } from "../components/ChatComposer.js";
import { TontoBot } from "../components/TontoBot.js";
import { TontoLogo } from "../components/TontoLogo.js";
import type { useConversation } from "../features/conversation/useConversation.js";
import {
  calculateDurationProgress,
  formatRecordingDurationLabel,
} from "../lib/audio.js";
import type { BackendStatus } from "../types/conversation.js";

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
    <main className="min-h-screen bg-slate-950 p-5 pt-24 text-white">
      <div className="mx-auto grid min-h-[calc(100vh-7.25rem)] max-w-[100rem] gap-5 xl:grid-cols-[minmax(0,1fr)_25rem]">
        <section className="relative overflow-hidden rounded-[2rem] bg-gradient-to-br from-slate-900 via-slate-950 to-blue-950 p-7 shadow-2xl shadow-black/40">
          <div className="absolute inset-x-0 top-0 h-48 bg-mint-200/10" />
          <div className="relative z-10 flex flex-wrap items-center justify-between gap-4">
            <TontoLogo />
            <VoiceStatusSummary conversation={conversation} />
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
                  "Pulsa Escuchar y cuentame tu pregunta. Estoy listo para aprender contigo."}
              </div>
              {conversation.voice.captureStatus === "recording" ? (
                <MainRecordingIndicator
                  elapsedMs={conversation.voice.recordingElapsedMs}
                  limitMs={conversation.voice.recordingLimitMs}
                />
              ) : null}
              {conversation.voice.notice ? (
                <p className="mt-4 rounded-2xl bg-amber-50 px-5 py-3 text-base font-black text-amber-800">
                  {conversation.voice.notice}
                </p>
              ) : null}
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
              hint="Pulsa y habla"
              label="Escuchar"
              onClick={() => void conversation.startVoiceTurn()}
              tone="mint"
            />
            <ActionButton
              hint="Cuando termines"
              label="Enviar voz"
              onClick={() => void conversation.stopVoiceTurn()}
              tone="coral"
            />
            <ActionButton
              hint="Oir otra vez"
              label="Repetir"
              onClick={conversation.repeatLatest}
              tone="purple"
            />
            <ActionButton
              hint="Cancelar"
              label="Parar"
              onClick={conversation.cancelVoiceTurn}
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

function VoiceStatusSummary({
  conversation,
}: {
  conversation: ReturnType<typeof useConversation>;
}) {
  const { voice } = conversation;
  const overallTone = getOverallStatusTone(conversation);

  return (
    <details className="group w-full max-w-full sm:w-auto">
      <summary className="flex cursor-pointer list-none flex-wrap items-center gap-2 rounded-2xl border border-white/15 bg-white/8 px-4 py-3 text-xs font-bold text-white shadow-sm backdrop-blur transition hover:bg-white/12">
        <StatusDot label="Estado" tone={overallTone} />
      </summary>

      <div className="mt-3 grid gap-2 rounded-2xl border border-white/15 bg-slate-950/90 p-4 text-sm text-white shadow-xl shadow-black/20 backdrop-blur sm:min-w-80">
        <StatusDetail
          label="Backend"
          value={getBackendStatusLabel(conversation.backendStatus)}
        />
        <StatusDetail label="Captura" value={voice.captureStatus} />
        <StatusDetail label="Speech" value={voice.speechStatus} />
        <StatusDetail label="Permiso mic" value={voice.microphonePermission} />
        <StatusDetail label="Contrato" value={`${voice.sampleRateHz} Hz / ${voice.channels} ch`} />
        <StatusDetail label="HTTP audio" value={voice.httpStatus === null ? "--" : String(voice.httpStatus)} />
        <StatusDetail label="Latencia" value={voice.latencyMs === null ? "--" : `${voice.latencyMs} ms`} />
      </div>
    </details>
  );
}

function getOverallStatusTone(
  conversation: ReturnType<typeof useConversation>,
) {
  const { voice } = conversation;
  const backendOk = conversation.backendStatus === "connected";
  const backendBad = conversation.backendStatus === "disconnected";
  const microphoneOk = voice.microphoneSupported;
  const microphoneBad =
    !voice.microphoneSupported ||
    voice.microphonePermission === "denied" ||
    voice.captureStatus === "error";
  const speechOk = voice.speechSupported && voice.speechStatus !== "error";
  const speechBad = !voice.speechSupported || voice.speechStatus === "error";

  if (backendOk && microphoneOk && speechOk) {
    return "green";
  }

  if (backendBad && microphoneBad && speechBad) {
    return "rose";
  }

  return "amber";
}

function getBackendStatusLabel(status: BackendStatus) {
  const labels: Record<BackendStatus, string> = {
    checking: "Backend comprobando",
    connected: "Backend conectado",
    disconnected: "Backend desconectado",
  };

  return labels[status];
}

function getBackendStatusTone(status: BackendStatus) {
  if (status === "connected") {
    return "green";
  }
  if (status === "checking") {
    return "amber";
  }
  return "rose";
}

function StatusDot({
  label,
  tone,
}: {
  label: string;
  tone: "green" | "amber" | "rose";
}) {
  const dotClass = {
    green: "bg-emerald-400",
    amber: "bg-amber-300",
    rose: "bg-rose-400",
  }[tone];

  return (
    <span className="inline-flex items-center gap-2 whitespace-nowrap">
      <span className={`h-2.5 w-2.5 rounded-full ${dotClass}`} />
      {label}
    </span>
  );
}

function StatusDetail({ label, value }: { label: string; value: string }) {
  return (
    <div className="grid grid-cols-[6.5rem_minmax(0,1fr)] gap-3">
      <span className="text-white/55">{label}</span>
      <span className="break-words font-semibold text-white">{value}</span>
    </div>
  );
}

function MainRecordingIndicator({
  elapsedMs,
  limitMs,
}: {
  elapsedMs: number;
  limitMs: number;
}) {
  const progress = calculateDurationProgress(elapsedMs, limitMs);
  const durationLabel = formatRecordingDurationLabel(elapsedMs, limitMs);

  return (
    <div
      aria-label={`TONTO esta escuchando ${durationLabel}`}
      className="mt-4 rounded-3xl border border-emerald-200 bg-emerald-50 px-5 py-4 text-emerald-800"
      role="status"
    >
      <div className="flex flex-wrap items-center justify-between gap-3">
        <p className="text-lg font-black">TONTO esta escuchando</p>
        <p className="text-2xl font-black tabular-nums">
          {durationLabel}
        </p>
      </div>
      <div className="mt-3 h-3 overflow-hidden rounded-full bg-emerald-100">
        <div
          className="h-full rounded-full bg-emerald-500 transition-[width] duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>
      <p className="mt-3 text-sm font-bold">
        La grabacion se detiene sola al llegar al limite. Pulsa Enviar voz para mandarla.
      </p>
    </div>
  );
}

function ActionButton({
  hint,
  label,
  onClick,
  tone,
}: {
  hint: string;
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
      aria-label={`${label}: ${hint}`}
      className={`flex min-h-24 flex-col items-center justify-center rounded-3xl px-4 py-4 text-center shadow-xl transition hover:-translate-y-0.5 ${toneClass}`}
      onClick={onClick}
      title={`${label}: ${hint}`}
      type="button"
    >
      <span className="text-xl font-black leading-tight">{label}</span>
      <span className="mt-2 text-sm font-bold leading-tight opacity-80">
        {hint}
      </span>
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
