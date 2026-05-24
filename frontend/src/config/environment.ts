const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

function dashboardWebSocketUrl() {
  const configured = import.meta.env.VITE_DASHBOARD_WS_URL ?? import.meta.env.VITE_WS_BASE_URL;
  if (configured) {
    return configured.endsWith("/ws/dashboard") ? configured : `${configured.replace(/\/$/, "")}/ws/dashboard`;
  }

  const url = new URL(apiBaseUrl);
  url.protocol = url.protocol === "https:" ? "wss:" : "ws:";
  url.pathname = `${url.pathname.replace(/\/$/, "")}/ws/dashboard`;
  url.search = "";
  url.hash = "";
  return url.toString();
}

export const config = {
  apiBaseUrl,
  dashboardWebSocketUrl: dashboardWebSocketUrl(),
};
