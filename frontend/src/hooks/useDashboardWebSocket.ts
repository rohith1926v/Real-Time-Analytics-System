import { useEffect, useRef, useState } from "react";

import { config } from "../config/environment";
import type { DashboardLiveMessage } from "../types/dashboard";

export function useDashboardWebSocket() {
  const [message, setMessage] = useState<DashboardLiveMessage | null>(null);
  const [status, setStatus] = useState<"connecting" | "connected" | "fallback">("connecting");
  const retryRef = useRef<number>();
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    let closed = false;

    function connect() {
      if (closed) return;
      setStatus("connecting");
      const socket = new WebSocket(config.dashboardWebSocketUrl);
      socketRef.current = socket;

      socket.onopen = () => {
        if (!closed) setStatus("connected");
      };
      socket.onmessage = (event) => {
        if (!closed) setMessage(JSON.parse(event.data));
      };
      socket.onerror = () => {
        socket.close();
      };
      socket.onclose = () => {
        if (!closed) {
          setStatus("fallback");
          retryRef.current = window.setTimeout(connect, 3000);
        }
      };
    }

    connect();
    return () => {
      closed = true;
      if (retryRef.current) window.clearTimeout(retryRef.current);
      socketRef.current?.close();
    };
  }, []);

  return { message, status };
}
