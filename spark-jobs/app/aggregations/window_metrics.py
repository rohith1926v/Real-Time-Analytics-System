from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from app.config.settings import SparkStreamingSettings


def build_window_metrics(enriched_events: DataFrame, settings: SparkStreamingSettings) -> DataFrame:
    return (
        enriched_events.withWatermark("event_timestamp", settings.watermark_delay)
        .groupBy(F.window("event_timestamp", "5 minutes"), F.col("event_type"))
        .agg(
            F.count("*").alias("event_count"),
            F.sum(F.when(F.col("risk_score") >= 70, 1).otherwise(0)).alias("high_risk_event_count"),
            F.avg("risk_score").alias("risk_score_moving_average"),
            F.avg("response_time_ms").alias("avg_api_response_time"),
            F.avg(F.coalesce(F.col("bytes_sent"), F.lit(0)) + F.coalesce(F.col("bytes_received"), F.lit(0))).alias("avg_network_bytes"),
            F.sum(F.when(F.col("event_type") == "anomaly", 1).otherwise(0)).alias("anomaly_frequency"),
        )
        .select(
            F.lit("window_metrics").alias("metric_type"),
            F.col("window.start").alias("window_start"),
            F.col("window.end").alias("window_end"),
            "event_type",
            "event_count",
            "high_risk_event_count",
            F.round("risk_score_moving_average", 4).alias("risk_score_moving_average"),
            F.round("avg_api_response_time", 4).alias("avg_api_response_time"),
            F.round("avg_network_bytes", 4).alias("avg_network_bytes"),
            "anomaly_frequency",
            F.current_timestamp().alias("calculated_at"),
        )
    )


def build_risk_metrics(enriched_events: DataFrame, settings: SparkStreamingSettings) -> DataFrame:
    return (
        enriched_events.withWatermark("event_timestamp", settings.watermark_delay)
        .groupBy(F.window("event_timestamp", "1 minute", "30 seconds"), F.coalesce(F.col("source_ip"), F.lit("unknown")).alias("entity_id"))
        .agg(
            F.count("*").alias("rolling_event_count"),
            F.sum(F.when(F.col("risk_score") >= 70, 1).otherwise(0)).alias("high_risk_event_count"),
            F.avg("risk_score").alias("risk_score_moving_average"),
            F.approx_count_distinct("event_type").alias("event_type_diversity"),
        )
        .select(
            F.lit("risk_metrics").alias("metric_type"),
            F.col("window.start").alias("window_start"),
            F.col("window.end").alias("window_end"),
            "entity_id",
            "rolling_event_count",
            "high_risk_event_count",
            F.round("risk_score_moving_average", 4).alias("risk_score_moving_average"),
            "event_type_diversity",
            F.current_timestamp().alias("calculated_at"),
        )
    )
