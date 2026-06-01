import type { ActivityEvent } from "../types/conversation.js";

type ActivityTimelineProps = {
  events: ActivityEvent[];
};

const toneByKind: Record<ActivityEvent["kind"], string> = {
  listening: "border-mint-300 bg-mint-300",
  recording: "border-sky-300 bg-sky-300",
  uploading: "border-amber-300 bg-amber-300",
  transcribing: "border-emerald-300 bg-emerald-300",
  "user-message": "border-coral-300 bg-coral-300",
  thinking: "border-purple-300 bg-purple-300",
  response: "border-sky-300 bg-sky-300",
  speaking: "border-indigo-300 bg-indigo-300",
  error: "border-rose-300 bg-rose-300",
};

export function ActivityTimeline({ events }: ActivityTimelineProps) {
  return (
    <div className="space-y-4">
      {events.map((event) => (
        <div className="grid grid-cols-[1.25rem_1fr] gap-4" key={event.id}>
          <div className="relative flex justify-center">
            <span
              className={`mt-2 h-4 w-4 rounded-full border-4 ${toneByKind[event.kind]}`}
            />
            <span className="absolute top-7 h-[calc(100%+0.5rem)] w-px bg-white/25" />
          </div>
          <div className="rounded-2xl bg-white/92 p-4 text-slate-900 shadow-lg shadow-slate-950/10">
            <div className="flex items-center justify-between gap-3">
              <p className="text-sm font-bold text-slate-800">{event.label}</p>
              <time className="text-xs text-slate-500">
                {formatTime(event.createdAt)}
              </time>
            </div>
            <p className="mt-1 line-clamp-2 text-sm text-slate-600">
              {event.detail}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}

function formatTime(date: Date) {
  return date.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}
