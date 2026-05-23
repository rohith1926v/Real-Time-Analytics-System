import { Navigate, Route, Routes } from "react-router-dom";

import { DashboardLayout } from "./layouts/DashboardLayout";
import { OverviewPage } from "./pages/OverviewPage";

export default function App() {
  return (
    <Routes>
      <Route element={<DashboardLayout />}>
        <Route index element={<OverviewPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
