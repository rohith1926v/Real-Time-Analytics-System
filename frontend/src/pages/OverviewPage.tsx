import { Activity, CheckCircle2, CircleDashed, Server, ShieldCheck } from "lucide-react";

import { StatusCard } from "../components/StatusCard";
import { useHealthStatus } from "../hooks/useHealthStatus";

const platformCapabilities = [
  { name: "API Gateway Foundation", status: "Online", icon: Server },
  { name: "Frontend Console Shell", status: "Online", icon: Activity },
  { name: "Environment Configuration", status: "Ready", icon: ShieldCheck },
  { name: "Streaming Runtime", status: "Planned", icon: CircleDashed },
];

export function OverviewPage() {
  const health = useHealthStatus();

  return (
    <div className="space-y-6">
      <section className="grid gap-4 xl:grid-cols-[1.4fr_0.6fr]">
        <div className="rounded-lg border border-white/10 bg-surface-900 p-6 shadow-panel">
          <div className="flex flex-col gap-5 md:flex-row md:items-start md:justify-between">
            <div>
              <p className="text-sm font-medium text-cyan-200">Platform Readiness</p>
              <h2 className="mt-3 max-w-3xl text-3xl font-semibold text-white md:text-4xl">
                Phase 1 control plane is ready for distributed analytics expansion.
              </h2>
              <p className="mt-4 max-w-2xl text-sm leading-6 text-slate-400">
                The foundation separates UI, API, service, and infrastructure concerns so Kafka,
                Spark, ML inference, and operational storage can be added behind stable boundaries.
              </p>
            </div>
            <div className="rounded-md border border-emerald-400/20 bg-emerald-400/10 px-4 py-3 text-sm text-emerald-200">
              <div className="flex items-center gap-2">
                <CheckCircle2 size={16} />
                Foundation active
              </div>
            </div>
          </div>
        </div>

        <div className="rounded-lg border border-white/10 bg-surface-900 p-6 shadow-panel">
          <p className="text-sm font-medium text-slate-300">Backend Health</p>
          <div className="mt-5 space-y-3">
            <p className="text-2xl font-semibold text-white">
              {health.isLoading ? "Checking..." : health.data?.status ?? "Unavailable"}
            </p>
            <p className="text-sm text-slate-400">
              {health.error ?? health.data?.service ?? "Waiting for API response"}
            </p>
            <p className="text-xs uppercase tracking-wide text-slate-500">
              {health.data ? `${health.data.environment} / v${health.data.version}` : "No response metadata"}
            </p>
          </div>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {platformCapabilities.map((capability) => (
          <StatusCard
            key={capability.name}
            icon={capability.icon}
            name={capability.name}
            status={capability.status}
          />
        ))}
      </section>

      <section className="rounded-lg border border-white/10 bg-surface-900 p-6 shadow-panel">
        <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
          <div>
            <h2 className="text-lg font-semibold text-white">Engineering Workstreams</h2>
            <p className="mt-1 text-sm text-slate-400">Phase boundaries for the distributed analytics platform.</p>
          </div>
        </div>
        <div className="mt-5 grid gap-3 md:grid-cols-3">
          {["Kafka ingestion", "Spark processing", "ML anomaly detection"].map((item) => (
            <div key={item} className="rounded-md border border-white/10 bg-white/[0.03] p-4">
              <p className="text-sm font-medium text-white">{item}</p>
              <p className="mt-2 text-sm text-slate-500">Reserved for upcoming implementation phases.</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
