export interface HealthCheckResponse {
  status: string;
  service: string;
  environment: string;
  version: string;
  timestamp: string;
}
