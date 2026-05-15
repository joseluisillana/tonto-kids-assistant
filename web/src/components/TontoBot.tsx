import type { ConversationStatus } from "../types/conversation";

type TontoBotProps = {
  status: ConversationStatus;
  size?: "compact" | "large";
};

export function TontoBot({ status, size = "large" }: TontoBotProps) {
  const isActive = ["listening", "thinking", "speaking", "sending"].includes(
    status,
  );
  const sizeClass = size === "large" ? "h-72 w-72" : "h-40 w-40";

  return (
    <div className="relative grid place-items-center">
      <div
        className={`${sizeClass} relative rounded-[3.5rem] border-8 border-mint-200 bg-mint-300 shadow-2xl shadow-cyan-900/30`}
      >
        <div className="absolute -top-10 left-1/2 h-12 w-4 -translate-x-1/2 rounded-full bg-mint-200">
          <div className="absolute -top-7 left-1/2 h-10 w-10 -translate-x-1/2 rounded-full bg-coral-400 shadow-lg shadow-coral-500/40" />
        </div>
        <div className="absolute -left-8 top-1/3 h-20 w-9 rounded-l-3xl bg-coral-400" />
        <div className="absolute -right-8 top-1/3 h-20 w-9 rounded-r-3xl bg-coral-400" />
        <div className="absolute inset-7 rounded-[2.5rem] bg-slate-950 shadow-inner shadow-black">
          <div className="absolute left-16 top-20 h-16 w-9 rounded-full bg-cyan-200 shadow-lg shadow-cyan-300/50" />
          <div className="absolute right-16 top-20 h-16 w-9 rounded-full bg-cyan-200 shadow-lg shadow-cyan-300/50" />
          <div className="absolute bottom-20 left-1/2 h-7 w-20 -translate-x-1/2 rounded-b-full border-b-8 border-cyan-200" />
          {isActive ? (
            <div className="absolute inset-x-12 bottom-9 flex items-end justify-center gap-1">
              {Array.from({ length: 9 }).map((_, index) => (
                <span
                  className="w-2 rounded-full bg-mint-200"
                  key={index}
                  style={{ height: `${14 + ((index * 9) % 32)}px` }}
                />
              ))}
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}
