import type { ConversationStatus } from "../types/conversation.js";

type TontoBotProps = {
  status: ConversationStatus;
  size?: "compact" | "large";
};

export function TontoBot({ status, size = "large" }: TontoBotProps) {
  const isActive = ["listening", "thinking", "speaking", "sending"].includes(
    status,
  );
  const sizeClass = size === "large" ? "h-72 w-72" : "h-40 w-40";
  const isCompact = size === "compact";

  return (
    <div className="relative grid place-items-center">
      <div
        className={`${sizeClass} relative rounded-[3.5rem] border-8 border-mint-200 bg-mint-300 shadow-2xl shadow-cyan-900/30 transition-transform duration-300 ${
          isActive ? "scale-[1.02]" : ""
        }`}
      >
        <div className="absolute -top-10 left-1/2 h-12 w-4 -translate-x-1/2 rounded-full bg-mint-200">
          <div
            className={`absolute -top-7 left-1/2 h-10 w-10 -translate-x-1/2 rounded-full bg-coral-400 shadow-lg shadow-coral-500/40 ${
              isActive ? "animate-pulse" : ""
            }`}
          />
        </div>
        <div className="absolute -left-8 top-1/3 h-20 w-9 rounded-l-3xl bg-coral-400" />
        <div className="absolute -right-8 top-1/3 h-20 w-9 rounded-r-3xl bg-coral-400" />
        <div className="absolute inset-7 rounded-[2.5rem] bg-slate-950 shadow-inner shadow-black">
          <BotBrows status={status} />
          <BotEyes status={status} />
          <BotMouth isCompact={isCompact} status={status} />
        </div>
      </div>
    </div>
  );
}

function BotBrows({ status }: { status: ConversationStatus }) {
  const browBase =
    "absolute top-[23%] h-[10%] w-[18%] rounded-full border-t-4 border-cyan-100 shadow-md shadow-cyan-300/40";

  if (status === "error") {
    return (
      <>
        <div className={`${browBase} left-[25%] rotate-[18deg]`} />
        <div className={`${browBase} right-[25%] -rotate-[18deg]`} />
      </>
    );
  }

  if (status === "thinking" || status === "sending") {
    return (
      <>
        <div className={`${browBase} left-[26%] tonto-brow-thinking -rotate-6`} />
        <div className={`${browBase} right-[26%] tonto-brow-thinking rotate-6`} />
      </>
    );
  }

  if (status === "speaking") {
    return (
      <>
        <div className={`${browBase} left-[26%] tonto-brow-speaking -rotate-12`} />
        <div className={`${browBase} right-[26%] tonto-brow-speaking rotate-12`} />
      </>
    );
  }

  if (status === "listening") {
    return (
      <>
        <div className={`${browBase} left-[27%] tonto-brow-listening -rotate-6`} />
        <div className={`${browBase} right-[27%] tonto-brow-listening rotate-6`} />
      </>
    );
  }

  return (
    <>
      <div className={`${browBase} left-[26%] -rotate-12`} />
      <div className={`${browBase} right-[26%] rotate-12`} />
    </>
  );
}

function BotEyes({ status }: { status: ConversationStatus }) {
  if (status === "thinking" || status === "sending") {
    return (
      <>
        <div className="absolute left-[28%] top-[40%] h-[8%] w-[15%] rounded-full bg-cyan-200 shadow-lg shadow-cyan-300/50" />
        <div className="absolute right-[28%] top-[40%] h-[8%] w-[15%] rounded-full bg-cyan-200 shadow-lg shadow-cyan-300/50" />
      </>
    );
  }

  if (status === "error") {
    return (
      <>
        <div className="absolute left-[28%] top-[38%] h-[8%] w-[17%] rotate-12 rounded-full bg-rose-300 shadow-lg shadow-rose-300/40" />
        <div className="absolute right-[28%] top-[38%] h-[8%] w-[17%] -rotate-12 rounded-full bg-rose-300 shadow-lg shadow-rose-300/40" />
      </>
    );
  }

  if (status === "listening") {
    return (
      <>
        <div className="absolute left-[28%] top-[40%] h-[8%] w-[15%] rounded-full bg-cyan-200 shadow-lg shadow-cyan-300/50 tonto-eye-blink tonto-eye-listening" />
        <div className="absolute right-[28%] top-[40%] h-[8%] w-[15%] rounded-full bg-cyan-200 shadow-lg shadow-cyan-300/50 tonto-eye-blink tonto-eye-listening" />
      </>
    );
  }

  const eyeMotionClass =
    status === "idle" ? "tonto-eye-blink" : "";

  return (
    <>
      <div
        className={`absolute left-[29%] top-[35%] h-[25%] w-[13%] rounded-full bg-cyan-200 shadow-lg shadow-cyan-300/50 transition-transform ${eyeMotionClass}`}
      />
      <div
        className={`absolute right-[29%] top-[35%] h-[25%] w-[13%] rounded-full bg-cyan-200 shadow-lg shadow-cyan-300/50 transition-transform ${eyeMotionClass}`}
      />
    </>
  );
}

function BotMouth({
  isCompact,
  status,
}: {
  isCompact: boolean;
  status: ConversationStatus;
}) {
  if (status === "speaking") {
    return (
      <div className="absolute bottom-[16%] left-1/2 h-[24%] w-[38%] -translate-x-1/2">
        <div className="tonto-speaking-mouth-fill absolute inset-x-[8%] top-[30%] h-[68%] bg-cyan-100 shadow-lg shadow-cyan-300/40" />
        <div className="tonto-speaking-mouth-lip absolute inset-x-0 top-0 h-[46%] rounded-b-full border-b-8 border-cyan-100 shadow-md shadow-cyan-300/30" />
      </div>
    );
  }

  if (status === "thinking" || status === "sending") {
    return (
      <div className="absolute bottom-[23%] left-1/2 h-6 w-16 -translate-x-1/2">
        <div className="tonto-thinking-mouth h-full w-full rounded-b-full border-b-8 border-cyan-200 shadow-md shadow-cyan-300/40" />
      </div>
    );
  }

  if (status === "listening") {
    return (
      <div className="absolute bottom-[23%] left-1/2 h-6 w-16 -translate-x-1/2">
        <div className="tonto-listening-mouth h-full w-full rounded-b-full border-b-8 border-cyan-200 shadow-md shadow-cyan-300/40" />
      </div>
    );
  }

  if (status === "error") {
    return (
      <div className="absolute bottom-[22%] left-1/2 h-[12%] w-[28%] -translate-x-1/2 rounded-t-full border-t-8 border-rose-300" />
    );
  }

  return (
    <div
      className={`absolute bottom-[22%] left-1/2 -translate-x-1/2 rounded-b-full border-b-8 border-cyan-200 ${
        isCompact ? "h-4 w-12" : "h-7 w-20"
      }`}
    />
  );
}
