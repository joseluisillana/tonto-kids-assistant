import {
  calculateDurationProgress,
  formatBytes,
  formatRecordingDurationLabel,
} from "../lib/audio.js";
import type { useConversation } from "../features/conversation/useConversation.js";

type VoiceLoopPanelProps = {
  conversation: ReturnType<typeof useConversation>;
  compact?: boolean;
};

export function VoiceLoopPanel({
  conversation,
  compact = false,
}: VoiceLoopPanelProps) {
  const { voice } = conversation;

  return (
    <section
      className={`rounded-[2rem] border border-slate-200 bg-white ${
        compact ? "p-5" : "p-6"
      } shadow-sm`}
    >
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h2 className={`${compact ? "text-lg" : "text-2xl"} font-black text-blue-950`}>
            Loop de voz
          </h2>
          <p className="mt-1 text-sm text-slate-500">
            Micrófono del navegador, WAV PCM 16 kHz y speech nativo.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <StatusChip
            label={
              voice.microphoneSupported
                ? "Microfono OK"
                : "Sin microfono"
            }
            tone={voice.microphoneSupported ? "green" : "rose"}
          />
          <StatusChip
            label={
              voice.speechSupported ? "Speech OK" : "Speech no soportado"
            }
            tone={voice.speechSupported ? "green" : "amber"}
          />
          <StatusChip
            label={voice.captureStatus}
            tone={statusTone(voice.captureStatus)}
          />
        </div>
      </div>

      <div className={`mt-5 grid gap-4 ${compact ? "" : "lg:grid-cols-2"}`}>
        {voice.captureStatus === "recording" ? (
          <ListeningIndicator
            elapsedMs={voice.recordingElapsedMs}
            limitMs={voice.recordingLimitMs}
          />
        ) : null}
        {voice.notice ? <NoticeBlock value={voice.notice} /> : null}
        <InfoBlock
          label="Estado tecnico"
          value={`${voice.captureStatus} / ${voice.speechStatus}`}
          hint={`Permiso ${voice.microphonePermission} | backend ${voice.backendUrl}`}
        />
        <InfoBlock
          label="Latencia"
          value={voice.latencyMs === null ? "--" : `${voice.latencyMs} ms`}
          hint={
            voice.httpStatus === null
              ? "HTTP pendiente"
              : `HTTP ${voice.httpStatus}`
          }
        />
        <InfoBlock
          label="Duracion"
          value={voice.durationMs === null ? "--" : `${voice.durationMs} ms`}
          hint={
            voice.wavBytes === null
              ? "Sin WAV aun"
              : `${formatBytes(voice.wavBytes)} generados`
          }
        />
        <InfoBlock
          label="Contrato"
          value={`${voice.sampleRateHz} Hz / ${voice.channels} ch`}
          hint={`device_id ${voice.deviceId}`}
        />
      </div>

      <div className="mt-5 grid gap-4 lg:grid-cols-2">
        <PanelBlock label="Transcript" value={voice.transcript} />
        <PanelBlock label="Response" value={voice.response} />
      </div>

      {voice.error ? (
        <p className="mt-4 rounded-2xl bg-rose-50 px-4 py-3 text-sm font-semibold text-rose-700">
          {voice.error}
        </p>
      ) : null}

      {!compact ? (
        <dl className="mt-6 grid gap-3 text-sm text-slate-600 md:grid-cols-2 xl:grid-cols-3">
          <DetailRow label="session_id" value={conversation.sessionId} />
          <DetailRow label="device_id" value={voice.deviceId} />
          <DetailRow label="language" value={voice.language} />
          <DetailRow label="mime" value={voice.wavMimeType ?? "--"} />
          <DetailRow
            label="mic permission"
            value={voice.microphonePermission}
          />
          <DetailRow label="speech voice" value={voice.speechVoice ?? "--"} />
        </dl>
      ) : null}
    </section>
  );
}

function ListeningIndicator({
  elapsedMs,
  limitMs,
}: {
  elapsedMs: number;
  limitMs: number;
}) {
  const progress = calculateDurationProgress(elapsedMs, limitMs);
  const label = `Escuchando... ${formatRecordingDurationLabel(elapsedMs, limitMs)}`;

  return (
    <div
      aria-label={label}
      className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-emerald-800 lg:col-span-2"
      role="status"
    >
      <div className="flex flex-wrap items-center justify-between gap-3">
        <p className="text-sm font-black">{label}</p>
        <p className="text-xs font-bold uppercase tracking-wide text-emerald-700">
          TONTO está escuchando
        </p>
      </div>
      <div className="mt-3 h-2 overflow-hidden rounded-full bg-emerald-100">
        <div
          className="h-full rounded-full bg-emerald-500 transition-[width] duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  );
}

function StatusChip({
  label,
  tone,
}: {
  label: string;
  tone: "green" | "amber" | "rose" | "blue";
}) {
  const classes = {
    green: "bg-emerald-50 text-emerald-700 border-emerald-200",
    amber: "bg-amber-50 text-amber-700 border-amber-200",
    rose: "bg-rose-50 text-rose-700 border-rose-200",
    blue: "bg-sky-50 text-sky-700 border-sky-200",
  }[tone];

  return (
    <span className={`rounded-full border px-3 py-1 text-xs font-bold ${classes}`}>
      {label}
    </span>
  );
}

function InfoBlock({
  label,
  value,
  hint,
}: {
  label: string;
  value: string;
  hint: string;
}) {
  return (
    <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
      <p className="text-xs font-bold uppercase tracking-wide text-slate-500">
        {label}
      </p>
      <p className="mt-2 break-words text-lg font-black text-slate-950">{value}</p>
      <p className="mt-1 break-words text-sm text-slate-500">{hint}</p>
    </div>
  );
}

function PanelBlock({
  label,
  value,
}: {
  label: string;
  value: string | null;
}) {
  return (
    <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
      <p className="text-xs font-bold uppercase tracking-wide text-slate-500">
        {label}
      </p>
      <p className="mt-2 min-h-24 whitespace-pre-wrap break-words text-base leading-7 text-slate-900">
        {value?.trim() ? value : "Esperando audio..."}
      </p>
    </div>
  );
}

function DetailRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-slate-100 bg-slate-50 px-4 py-3">
      <dt className="text-xs font-bold uppercase tracking-wide text-slate-500">
        {label}
      </dt>
      <dd className="mt-1 break-all font-medium text-slate-900">{value}</dd>
    </div>
  );
}

function statusTone(status: string): "green" | "amber" | "rose" | "blue" {
  if (status === "complete" || status === "recording" || status === "ready-to-send") {
    return "green";
  }
  if (status === "error") {
    return "rose";
  }
  if (status === "requesting-permission" || status === "uploading") {
    return "amber";
  }
  return "blue";
}

function NoticeBlock({ value }: { value: string }) {
  return (
    <div
      className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm font-bold text-amber-800 lg:col-span-2"
      role="status"
    >
      {value}
    </div>
  );
}
