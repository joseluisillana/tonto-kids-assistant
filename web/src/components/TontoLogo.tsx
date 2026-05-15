export function TontoLogo({ variant = "dark" }: { variant?: "dark" | "light" }) {
  const textClass = variant === "dark" ? "text-white" : "text-coral-600";

  return (
    <div className="flex items-center gap-1 text-4xl font-black tracking-normal">
      <span className="text-mint-300">T</span>
      <span className="grid h-11 w-11 place-items-center rounded-full bg-white text-sm font-black text-slate-900 shadow-lg">
        TO
      </span>
      <span className="text-coral-400">N</span>
      <span className="text-amber-300">T</span>
      <span className={textClass}>O</span>
    </div>
  );
}
