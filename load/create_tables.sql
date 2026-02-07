-- Create analytics tables (run inside DB city_pulse)
CREATE TABLE IF NOT EXISTS bikes_analytics (
  city TEXT,
  station_id INT,
  station_name TEXT,
  available_bikes INT,
  bike_stands INT,
  status TEXT,
  datetime TIMESTAMP
);

CREATE TABLE IF NOT EXISTS weather_analytics (
  city TEXT,
  datetime TIMESTAMP,
  temp DOUBLE PRECISION,
  humidity INT,
  wind_speed DOUBLE PRECISION,
  weather TEXT
);

DROP TABLE IF EXISTS city_pulse_hourly;

CREATE TABLE city_pulse_hourly (
  city TEXT,
  date_hour TIMESTAMP,
  avg_temp DOUBLE PRECISION,
  avg_humidity DOUBLE PRECISION,
  avg_wind_speed DOUBLE PRECISION,
  weather_desc TEXT,
  total_available_bikes BIGINT,
  total_stands BIGINT,
  stations_count INT,
  availability_ratio NUMERIC(10,4)
);

CREATE INDEX IF NOT EXISTS idx_city_pulse_hourly_city_dt
ON city_pulse_hourly(city, date_hour);
