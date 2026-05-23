import type { LucideIcon } from "lucide-react";

interface StatusCardProps {
  icon: LucideIcon;
  name: string;
  status: string;
}

export function StatusCard({ icon: Icon, name, status }: StatusCardProps) {
  const isPlanned = status === "Planned";

  return (
    <article className="rounded-lg border border-white/10 bg-surface-900 p-5 shadow-panel">
      <div className="flex items-start justify-between gap-4">
        <div className="grid h-10 w-10 place-items-center rounded-md bg-white/5 text-cyan-200">
          <Icon size={18} />
        </div>
        <span
          className={`rounded-md px-2.5 py-1 text-xs font-medium ${
            isPlanned ? "bg-amber-400/10 text-amber-200" : "bg-emerald-400/10 text-emerald-200"
          }`}
        >
          {status}
        </span>
      </div>
      <h3 className="mt-5 text-sm font-semibold text-white">{name}</h3>
      <p className="mt-2 text-sm leading-6 text-slate-500">Provisioned as part of the Phase 1 platform baseline.</p>
    </article>
  );
}
