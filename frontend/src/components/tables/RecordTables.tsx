import { ChevronDown } from "lucide-react";
import { useState } from "react";

import type { AnalyticsRecord, EntityRiskPoint } from "../../types/dashboard";
import { SeverityBadge } from "../ui/SeverityBadge";

export function RecordsTable({ title, records }: { title: string; records: AnalyticsRecord[] }) {
  return (
    <section className="overflow-hidden rounded-lg border border-white/10 bg-surface-900 shadow-panel">
      <div className="border-b border-white/10 px-5 py-4">
        <h2 className="text-sm font-semibold text-white">{title}</h2>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[760px] text-left text-sm">
          <thead className="bg-white/[0.03] text-xs uppercase text-slate-500">
            <tr>
              <th className="px-5 py-3">Severity</th>
              <th className="px-5 py-3">Entity</th>
              <th className="px-5 py-3">Type</th>
              <th className="px-5 py-3">Risk</th>
              <th className="px-5 py-3">Topic</th>
              <th className="px-5 py-3">Timestamp</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/10">
            {records.length ? records.map((record, index) => <RecordRow key={`${record.id ?? index}-${record.timestamp}`} record={record} />) : <EmptyRow />}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function RecordRow({ record }: { record: AnalyticsRecord }) {
  const [open, setOpen] = useState(false);
  const risk = record.ml_risk_score ?? record.risk_score ?? Number(record.raw_payload?.ml_risk_score ?? record.raw_payload?.risk_score ?? 0);
  return (
    <>
      <tr className="text-slate-300">
        <td className="px-5 py-3"><SeverityBadge severity={record.severity ?? String(record.raw_payload?.severity ?? record.raw_payload?.risk_level ?? "low")} /></td>
        <td className="px-5 py-3 font-medium text-white">{record.entity_id ?? String(record.raw_payload?.entity_id ?? record.raw_payload?.source_ip ?? "unknown")}</td>
        <td className="px-5 py-3">{record.event_type ?? String(record.raw_payload?.event_type ?? "event")}</td>
        <td className="px-5 py-3">{risk ? risk.toFixed(1) : "0.0"}</td>
        <td className="px-5 py-3 text-slate-500">{record.source_topic ?? "stream"}</td>
        <td className="px-5 py-3 text-slate-500">{formatTime(record.timestamp ?? String(record.raw_payload?.timestamp ?? ""))}</td>
        <td className="px-5 py-3">
          <button className="grid h-8 w-8 place-items-center rounded-md bg-white/5 text-slate-300" onClick={() => setOpen((value) => !value)} type="button">
            <ChevronDown size={16} />
          </button>
        </td>
      </tr>
      {open ? (
        <tr>
          <td colSpan={7} className="bg-black/20 px-5 py-4">
            <pre className="max-h-52 overflow-auto rounded-md bg-surface-950 p-4 text-xs text-slate-300">{JSON.stringify(record.raw_payload, null, 2)}</pre>
          </td>
        </tr>
      ) : null}
    </>
  );
}

function EmptyRow() {
  return (
    <tr>
      <td colSpan={7} className="px-5 py-10 text-center text-slate-500">No records available yet. The dashboard will fill as the local pipeline persists data.</td>
    </tr>
  );
}

export function TopEntitiesTable({ entities }: { entities: EntityRiskPoint[] }) {
  return (
    <section className="rounded-lg border border-white/10 bg-surface-900 p-5 shadow-panel">
      <h2 className="text-sm font-semibold text-white">High-Risk Entities</h2>
      <div className="mt-4 space-y-3">
        {entities.map((entity) => (
          <div key={entity.entity_id} className="flex items-center justify-between gap-4 rounded-md bg-white/[0.03] px-4 py-3">
            <div>
              <p className="font-medium text-white">{entity.entity_id}</p>
              <p className="text-xs text-slate-500">{entity.event_count} observations</p>
            </div>
            <div className="flex items-center gap-3">
              <SeverityBadge severity={entity.severity} />
              <span className="text-sm font-semibold text-amber-200">{entity.risk_score.toFixed(1)}</span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function formatTime(value?: string | null) {
  if (!value) return "pending";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

