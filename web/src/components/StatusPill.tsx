import type { BackendStatus } from "../types/conversation.js";

type StatusPillProps = {
  status: BackendStatus;
};

const labels: Record<BackendStatus, string> = {
  checking: "Comprobando backend",
  connected: "Backend conectado",
  disconnected: "Backend desconectado",
};

const colorClasses: Record<BackendStatus, string> = {
  checking: "border-sky-300/40 text-sky-100",
  connected: "border-emerald-300/50 text-emerald-100",
  disconnected: "border-rose-300/50 text-rose-100",
};

const dotClasses: Record<BackendStatus, string> = {
  checking: "bg-sky-300",
  connected: "bg-emerald-400",
  disconnected: "bg-rose-400",
};

export function StatusPill({ status }: StatusPillProps) {
  return (
    <div
      className={`inline-flex items-center gap-3 rounded-full border bg-white/8 px-5 py-3 text-sm font-semibold shadow-sm backdrop-blur ${colorClasses[status]}`}
    >
      <span className={`h-3 w-3 rounded-full ${dotClasses[status]}`} />
      {labels[status]}
    </div>
  );
}
