from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum as _sum, avg, when, round

# 1. Initialisation de la session Spark
spark = SparkSession.builder \
    .appName("FlightDelayAnalytics") \
    .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.4.1") \
    .config("spark.cassandra.connection.host", "127.0.0.1") \
    .getOrCreate()

# 2. Ingestion des données CSV
df = spark.read.csv("Flight_delay.csv", header=True, inferSchema=True)

# 3. Filtrage et définition du retard important (> 60 minutes)
df_clean = df.filter((col("Cancelled") == 0) & col("ArrDelay").isNotNull()) \
             .withColumn("IS_SEVERE_DELAY", when(col("ArrDelay") > 60, 1).otherwise(0))

# KPI 1 : Taux de retards importants par aéroport et par date
kpi_airport = df_clean.groupBy("Origin", "Date") \
    .agg(
        count("*").alias("total_flights"),
        _sum("IS_SEVERE_DELAY").alias("delayed_flights"),
        round(avg("ArrDelay"), 2).alias("avg_delay_minutes"),
        round(_sum("IS_SEVERE_DELAY") / count("*"), 4).alias("delay_rate")
    ) \
    .withColumnRenamed("Origin", "airport_code") \
    .withColumnRenamed("Date", "flight_date")

# KPI 2 : Taux de retards importants par compagnie
kpi_airline = df_clean.groupBy("Airline") \
    .agg(
        count("*").alias("total_flights"),
        _sum("IS_SEVERE_DELAY").alias("delayed_flights"),
        round(avg("ArrDelay"), 2).alias("avg_delay_minutes"),
        round(_sum("IS_SEVERE_DELAY") / count("*"), 4).alias("delay_rate")
    ) \
    .withColumnRenamed("Airline", "airline")

# KPI 3 : Taux de retards importants par jour de la semaine
kpi_weekday = df_clean.groupBy("DayOfWeek") \
    .agg(
        count("*").alias("total_flights"),
        _sum("IS_SEVERE_DELAY").alias("delayed_flights"),
        round(avg("ArrDelay"), 2).alias("avg_delay_minutes"),
        round(_sum("IS_SEVERE_DELAY") / count("*"), 4).alias("delay_rate")
    ) \
    .withColumnRenamed("DayOfWeek", "day_of_week")

# 4. Écriture dans les tables Cassandra
tables = [
    (kpi_airport, "delays_by_airport"),
    (kpi_airline, "delays_by_airline"),
    (kpi_weekday, "delays_by_weekday")
]

for kpi_df, table_name in tables:
    kpi_df.write \
        .format("org.apache.spark.sql.cassandra") \
        .options(table=table_name, keyspace="flight_analytics") \
        .mode("append") \
        .save()

print("Mise à jour réussie : calculs des taux de retards importants (>60 min) insérés dans Cassandra.")
spark.stop()
