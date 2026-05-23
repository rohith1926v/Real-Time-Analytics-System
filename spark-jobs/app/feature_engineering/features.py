from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from app.config.settings import SparkStreamingSettings


def _feature_frame(df: DataFrame, feature_name: str, entity_column: str, value_column: str, count_column: str = "event_count") -> DataFrame:
    return df.select(
        F.lit(feature_name).alias("feature_name"),
        F.col(entity_column).cast("string").alias("entity_id"),
        F.col("window.start").alias("window_start"),
        F.col("window.end").alias("window_end"),
        F.round(F.col(value_column).cast("double"), 6).alias("feature_value"),
        F.col(count_column).cast("long").alias("event_count"),
        F.current_timestamp().alias("calculated_at"),
    )


def build_login_features(login_events: DataFrame, settings: SparkStreamingSettings) -> DataFrame:
    base = (
        login_events.withWatermark("event_timestamp", settings.watermark_delay)
        .groupBy(F.window("event_timestamp", "1 minute", "30 seconds"), F.coalesce(F.col("user_id"), F.lit("unknown")).alias("user_id"))
        .agg(
            F.count("*").alias("event_count"),
            F.sum(F.when(F.col("login_success") == F.lit(False), 1).otherwise(0)).alias("failed_login_count"),
            F.approx_count_distinct("country").alias("geo_login_variance"),
        )
        .withColumn("user_failed_login_rate", F.col("failed_login_count") / F.col("event_count"))
    )

    failed_rate = _feature_frame(base, "user_failed_login_rate", "user_id", "user_failed_login_rate")
    geo_variance = _feature_frame(base, "geo_login_variance", "user_id", "geo_login_variance")
    return failed_rate.unionByName(geo_variance)


def build_api_features(api_events: DataFrame, settings: SparkStreamingSettings) -> DataFrame:
    base = (
        api_events.withWatermark("event_timestamp", settings.watermark_delay)
        .groupBy(F.window("event_timestamp", "1 minute", "30 seconds"), F.coalesce(F.col("endpoint"), F.lit("unknown")).alias("endpoint"))
        .agg(
            F.count("*").alias("event_count"),
            F.avg("response_time_ms").alias("avg_api_response_time"),
            F.sum(F.when(F.col("status_code") >= 400, 1).otherwise(0)).alias("error_count"),
        )
        .withColumn("requests_per_minute", F.col("event_count").cast("double"))
        .withColumn("endpoint_error_rate", F.col("error_count") / F.col("event_count"))
    )

    response_time = _feature_frame(base, "avg_api_response_time", "endpoint", "avg_api_response_time")
    rpm = _feature_frame(base, "requests_per_minute", "endpoint", "requests_per_minute")
    error_rate = _feature_frame(base, "endpoint_error_rate", "endpoint", "endpoint_error_rate")
    return response_time.unionByName(rpm).unionByName(error_rate)


def build_network_features(network_events: DataFrame, settings: SparkStreamingSettings) -> DataFrame:
    base = (
        network_events.withWatermark("event_timestamp", settings.watermark_delay)
        .groupBy(F.window("event_timestamp", "1 minute", "30 seconds"), F.coalesce(F.col("source_ip"), F.lit("unknown")).alias("source_ip"))
        .agg(
            F.count("*").alias("event_count"),
            F.avg(F.coalesce(F.col("bytes_sent"), F.lit(0)) + F.coalesce(F.col("bytes_received"), F.lit(0))).alias("avg_network_bytes"),
            F.sum(F.when(F.col("risk_score") >= 70, 1).otherwise(0)).alias("suspicious_ip_frequency"),
        )
    )

    avg_bytes = _feature_frame(base, "avg_network_bytes", "source_ip", "avg_network_bytes")
    suspicious = _feature_frame(base, "suspicious_ip_frequency", "source_ip", "suspicious_ip_frequency")
    return avg_bytes.unionByName(suspicious)


def build_anomaly_features(anomaly_events: DataFrame, settings: SparkStreamingSettings) -> DataFrame:
    base = (
        anomaly_events.withWatermark("event_timestamp", settings.watermark_delay)
        .groupBy(F.window("event_timestamp", "1 minute", "30 seconds"), F.coalesce(F.col("anomaly_type"), F.lit("unknown")).alias("anomaly_type"))
        .agg(F.count("*").alias("event_count"), F.avg("risk_score").alias("anomaly_rate"))
    )
    return _feature_frame(base, "anomaly_rate", "anomaly_type", "anomaly_rate")


def build_feature_pipeline(
    login_events: DataFrame,
    api_events: DataFrame,
    network_events: DataFrame,
    anomaly_events: DataFrame,
    settings: SparkStreamingSettings,
) -> DataFrame:
    return (
        build_login_features(login_events, settings)
        .unionByName(build_api_features(api_events, settings))
        .unionByName(build_network_features(network_events, settings))
        .unionByName(build_anomaly_features(anomaly_events, settings))
    )
