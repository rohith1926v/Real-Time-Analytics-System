import { Navigate, Route, Routes } from "react-router-dom";

import { DashboardLayout } from "./layouts/DashboardLayout";
import { LiveStreamPage } from "./pages/LiveStreamPage";
import { MLPredictionsPage } from "./pages/MLPredictionsPage";
import { OverviewPage } from "./pages/OverviewPage";
import { RiskAnalyticsPage } from "./pages/RiskAnalyticsPage";
import { SearchPage } from "./pages/SearchPage";
import { SystemHealthPage } from "./pages/SystemHealthPage";

export default function App() {
  return (
    <Routes>
      <Route element={<DashboardLayout />}>
        <Route index element={<OverviewPage />} />
        <Route path="live" element={<LiveStreamPage />} />
        <Route path="risk" element={<RiskAnalyticsPage />} />
        <Route path="predictions" element={<MLPredictionsPage />} />
        <Route path="search" element={<SearchPage />} />
        <Route path="health" element={<SystemHealthPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
