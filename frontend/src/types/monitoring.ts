export interface ServiceHealth {
  name: string;
  status: string;
  detail: string;
  category: string;
  endpoint?: string | null;
  last_checked: string;
}

export interface MonitoringOverview {
  status: string;
  services_total: number;
  services_healthy: number;
  services_degraded: number;
  services_down: number;
  total_events: number;
  total_predictions: number;
  total_alerts: number;
  open_incidents: number;
  generated_at: string;
  prometheus_url: string;
  grafana_url: string;
}

export interface PipelineMetrics {
  telemetry_events: number;
  analytics_metrics: number;
  risk_metrics: number;
  feature_snapshots: number;
  anomaly_predictions: number;
  alerts: number;
  incidents: number;
  deadletter_events: number;
  generated_at: string;
}

export interface ErrorSummary {
  deadletter_events: number;
  critical_alerts: number;
  failed_services: number;
  degraded_services: number;
  recent_errors: Record<string, unknown>[];
  generated_at: string;
}

export interface MetricsSummary {
  prometheus_available: boolean;
  scraped_targets_up: number;
  scraped_targets_down: number;
  key_metrics: Record<string, number>;
  generated_at: string;
}
