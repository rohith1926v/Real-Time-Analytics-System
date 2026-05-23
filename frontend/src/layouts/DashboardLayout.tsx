import { Outlet } from "react-router-dom";
import { Activity, BarChart3, Bell, Database, LayoutDashboard, Search, Settings } from "lucide-react";

const navigationItems = [
  { label: "Overview", icon: LayoutDashboard, active: true },
  { label: "Streams", icon: Activity, active: false },
  { label: "Storage", icon: Database, active: false },
  { label: "Insights", icon: BarChart3, active: false },
  { label: "Settings", icon: Settings, active: false },
];

export function DashboardLayout() {
  return (
    <div className="min-h-screen bg-surface-950 text-slate-100">
      <aside className="fixed inset-y-0 left-0 z-30 hidden w-72 border-r border-white/10 bg-surface-900/95 px-5 py-6 lg:block">
        <div className="flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-md bg-cyan-400/15 text-cyan-300">
            <Activity size={22} />
          </div>
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-cyan-200">Streaming Analytics</p>
            <p className="text-xs text-slate-400">Enterprise Console</p>
          </div>
        </div>

        <nav className="mt-10 space-y-1">
          {navigationItems.map((item) => (
            <button
              key={item.label}
              className={`flex w-full items-center gap-3 rounded-md px-3 py-2.5 text-left text-sm transition ${
                item.active
                  ? "bg-cyan-400/12 text-cyan-100"
                  : "text-slate-400 hover:bg-white/5 hover:text-slate-100"
              }`}
              type="button"
            >
              <item.icon size={18} />
              <span>{item.label}</span>
            </button>
          ))}
        </nav>
      </aside>

      <div className="lg:pl-72">
        <header className="sticky top-0 z-20 border-b border-white/10 bg-surface-950/88 px-4 py-4 backdrop-blur md:px-8">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-xs font-medium uppercase tracking-wide text-slate-500">Phase 1 Foundation</p>
              <h1 className="mt-1 text-xl font-semibold text-white">Operational Control Plane</h1>
            </div>
            <div className="flex items-center gap-3">
              <div className="hidden min-w-72 items-center gap-2 rounded-md border border-white/10 bg-white/5 px-3 py-2 text-slate-400 md:flex">
                <Search size={16} />
                <span className="text-sm">Search services, streams, incidents</span>
              </div>
              <button className="grid h-10 w-10 place-items-center rounded-md border border-white/10 bg-white/5 text-slate-300" type="button" aria-label="Notifications">
                <Bell size={18} />
              </button>
            </div>
          </div>
        </header>

        <main className="px-4 py-6 md:px-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
