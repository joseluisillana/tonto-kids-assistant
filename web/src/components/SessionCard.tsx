import type { BackendStatus } from "../types/conversation";

type SessionCardProps = {
  backendStatus: BackendStatus;
  elapsedSeconds: number;
  latestLatencyMs: number | null;
  questionCount: number;
  sessionId: string;
};

export function SessionCard({
  backendStatus,
  elapsedSeconds,
  latestLatencyMs,
  questionCount,
  sessionId,
}: SessionCardProps) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-blue-600">Sesion demo</h2>
          <p className="mt-1 text-sm font-medium text-emerald-600">
            {backendStatus === "connected" ? "Activa" : "Pendiente"}
          </p>
        </div>
        <div className="grid h-14 w-14 place-items-center rounded-2xl bg-amber-300 text-xl font-black text-white">
          T
        </div>
      </div>

      <dl className="mt-6 space-y-4 text-sm">
        <Row label="Tiempo de sesion" value={formatDuration(elapsedSeconds)} />
        <Row label="Preguntas hechas" value={String(questionCount)} />
        <Row
          label="Latencia"
          value={latestLatencyMs === null ? "--" : `${latestLatencyMs} ms`}
        />
        <Row label="ID" value={sessionId.slice(0, 18)} />
      </dl>
    </section>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between gap-4 border-t border-slate-100 pt-4">
      <dt className="text-slate-500">{label}</dt>
      <dd className="text-right font-bold text-slate-800">{value}</dd>
    </div>
  );
}

function formatDuration(totalSeconds: number) {
  const minutes = Math.floor(totalSeconds / 60)
    .toString()
    .padStart(2, "0");
  const seconds = Math.floor(totalSeconds % 60)
    .toString()
    .padStart(2, "0");

  return `00:${minutes}:${seconds}`;
}
