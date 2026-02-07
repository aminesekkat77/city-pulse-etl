TRUNCATE TABLE city_pulse_hourly;

INSERT INTO city_pulse_hourly
WITH bikes_hourly AS (
  SELECT
    LOWER(city) AS city,
    date_trunc('hour', datetime) AS date_hour,
    SUM(available_bikes) AS total_available_bikes,
    SUM(bike_stands) AS total_stands,
    COUNT(DISTINCT station_id) AS stations_count,
    ROUND(SUM(available_bikes)::numeric / NULLIF(SUM(bike_stands),0), 4) AS availability_ratio
  FROM bikes_analytics
  GROUP BY 1, 2
),
weather_hourly AS (
  SELECT
    LOWER(city) AS city,
    date_trunc('hour', datetime) AS date_hour,
    AVG(temp) AS avg_temp,
    AVG(humidity) AS avg_humidity,
    AVG(wind_speed) AS avg_wind_speed,
    MAX(weather) AS weather_desc
  FROM weather_analytics
  GROUP BY 1, 2
)
SELECT
  b.city,
  b.date_hour,
  w.avg_temp,
  w.avg_humidity,
  w.avg_wind_speed,
  w.weather_desc,
  b.total_available_bikes,
  b.total_stands,
  b.stations_count,
  b.availability_ratio
FROM bikes_hourly b
INNER JOIN weather_hourly w
  ON b.city = w.city AND b.date_hour = w.date_hour;
