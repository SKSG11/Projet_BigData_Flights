-- Création du Keyspace
CREATE KEYSPACE IF NOT EXISTS flight_analytics 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE flight_analytics;

-- Table 1 : Taux de retard par aéroport et date (Partitionnée par aéroport)
CREATE TABLE IF NOT EXISTS delays_by_airport (
    airport_code text,
    flight_date text,
    total_flights int,
    avg_delay_minutes double,
    delay_rate double,
    PRIMARY KEY ((airport_code), flight_date)
) WITH CLUSTERING ORDER BY (flight_date DESC);

-- Table 2 : Taux de retard par compagnie aérienne
CREATE TABLE IF NOT EXISTS delays_by_airline (
    airline text,
    total_flights int,
    avg_delay_minutes double,
    delay_rate double,
    PRIMARY KEY (airline)
);

-- Table 3 : Taux de retard par jour de la semaine
CREATE TABLE IF NOT EXISTS delays_by_weekday (
    day_of_week int,
    total_flights int,
    avg_delay_minutes double,
    delay_rate double,
    PRIMARY KEY (day_of_week)
);
