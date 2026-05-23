import { httpClient } from "../api/httpClient";
import type { HealthCheckResponse } from "../types/health";

export async function getHealthStatus(): Promise<HealthCheckResponse> {
  const response = await httpClient.get<HealthCheckResponse>("/health");
  return response.data;
}
