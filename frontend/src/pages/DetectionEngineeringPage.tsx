import { Activity, FlaskConical, ShieldCheck, SlidersHorizontal } from "lucide-react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { MetricCard } from "../components/dashboard/MetricCard";
import { SeverityBadge } from "../components/ui/SeverityBadge";
import { useAsyncData } from "../hooks/useAsyncData";
import { threatIntelService } from "../services/threatIntelService";

export function DetectionEngineeringPage() {
  const rules = useAsyncData(threatIntelService.rules, [], 10_000);
  const stats = useAsyncData(threatIntelService.ruleStats, [], 10_000);
  return (
    <div className="space-y-6">
      <section className="rounded-lg border border-white/10 bg-surface-900 p-6 shadow-panel">
        <p className="text-sm font-medium text-cyan-200">Sigma-like Detection Rules</p>
        <h1 className="mt-2 text-2xl font-semibold text-white">Detection Engineering</h1>
        <p className="mt-2 text-sm text-slate-400">Local YAML rule management, hit analytics, pipeline health, and rule execution scoring.</p>
      </section>
      <section className="grid gap-4 md:grid-cols-3">
        <MetricCard label="Rules With Hits" value={rules.data?.length ?? 0} detail="Loaded rule families with observed matches." icon={ShieldCheck} />
        <MetricCard label="Total Rule Hits" value={stats.data?.total_rule_hits ?? 0} detail="Persisted detection rule hits." icon={Activity} tone="amber" />
        <MetricCard label="Pipeline Health" value="Active" detail="Threat engine executes YAML rules continuously." icon={FlaskConical} tone="emerald" />
      </section>
      <section className="grid gap-4 xl:grid-cols-[1fr_.9fr]">
        <article className="rounded-lg border border-white/10 bg-surface-900 p-5 shadow-panel">
          <h2 className="font-semibold text-white">Rule Hit Analytics</h2>
          <div className="mt-4 h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={rules.data ?? []}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,.15)" />
                <XAxis dataKey="rule_id" stroke="#94a3b8" tick={{ fontSize: 11 }} />
                <YAxis stroke="#94a3b8" />
                <Tooltip />
                <Bar dataKey="hit_count" fill="#22d3ee" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </article>
        <article className="rounded-lg border border-white/10 bg-surface-900 p-5 shadow-panel">
          <h2 className="flex items-center gap-2 font-semibold text-white"><SlidersHorizontal size={18} /> Rule Management</h2>
          <div className="mt-4 space-y-3">
            {(rules.data ?? []).map((rule) => (
              <div key={rule.rule_id} className="rounded-md border border-white/10 bg-white/[0.03] p-4">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="font-medium text-white">{rule.name}</p>
                    <p className="mt-1 font-mono text-xs text-slate-500">{rule.rule_id}</p>
                  </div>
                  <SeverityBadge severity={rule.severity} />
                </div>
                <div className="mt-3 flex items-center justify-between text-xs text-slate-400">
                  <span>{rule.hit_count} hits</span>
                  <span>avg score {rule.avg_score}</span>
                  <span className="text-emerald-300">{rule.enabled ? "enabled" : "disabled"}</span>
                </div>
              </div>
            ))}
          </div>
        </article>
      </section>
    </div>
  );
}
