import { useEffect, useState } from "react";

import { getHealthStatus } from "../services/healthService";
import type { HealthCheckResponse } from "../types/health";

interface HealthState {
  data: HealthCheckResponse | null;
  error: string | null;
  isLoading: boolean;
}

export function useHealthStatus(): HealthState {
  const [state, setState] = useState<HealthState>({
    data: null,
    error: null,
    isLoading: true,
  });

  useEffect(() => {
    let isMounted = true;

    getHealthStatus()
      .then((data) => {
        if (isMounted) {
          setState({ data, error: null, isLoading: false });
        }
      })
      .catch((error: unknown) => {
        if (isMounted) {
          setState({
            data: null,
            error: error instanceof Error ? error.message : "Unable to reach API",
            isLoading: false,
          });
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return state;
}
