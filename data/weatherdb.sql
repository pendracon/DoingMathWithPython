DROP DATABASE IF EXISTS weather;
CREATE DATABASE weather;
\c weather;

CREATE TYPE DataType
	AS ENUM (
		'HLY-CLOD-PCTBKN',
		'HLY-CLOD-PCTCLR',
		'HLY-CLOD-PCTFEW',
		'HLY-CLOD-PCTOVC',
		'HLY-CLOD-PCTSCT',
		'HLY-CLDH-NORMAL',
		'HLY-DEWP-10PCTL',
		'HLY-DEWP-90PCTL',
		'HLY-DEWP-NORMAL',
		'HLY-HIDX-NORMAL',
		'HLY-HTDH-NORMAL',
		'HLY-PRES-10PCTL',
		'HLY-PRES-90PCTL',
		'HLY-PRES-NORMAL',
		'HLY-TEMP-10PCTL',
		'HLY-TEMP-90PCTL',
		'HLY-TEMP-NORMAL',
		'HLY-WIND-1STDIR',
		'HLY-WIND-1STPCT',
		'HLY-WIND-2NDDIR',
		'HLY-WIND-2NDPCT',
		'HLY-WIND-AVGSPD',
		'HLY-WIND-PCTCLM',
		'HLY-WIND-VCTDIR',
		'HLY-WIND-VCTSPD',
		'HLY-WCHL-NORMAL'
	);

/*
 * Table for storing weather data type ids and descriptions.
 */
DROP TABLE IF EXISTS data_type;
CREATE TABLE data_type (
	data_type_id DataType PRIMARY KEY NOT NULL,
	descr VARCHAR(1024) NOT NULL
);

INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-CLOD-PCTBKN', 'Clouds broken percentage');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-CLOD-PCTCLR', 'Clouds clear percentage');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-CLOD-PCTFEW', 'Clouds few percentage');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-CLOD-PCTOVC', 'Clouds overcast percentage');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-CLOD-PCTSCT', 'Clouds scattered percentage');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-CLDH-NORMAL', 'Cooling degree hours');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-DEWP-10PCTL', 'Dew point 10th percentile');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-DEWP-90PCTL', 'Dew point 90th percentile');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-DEWP-NORMAL', 'Dew point mean');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-HIDX-NORMAL', 'Heat index mean');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-HTDH-NORMAL', 'Heating degree hours');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-PRES-10PCTL', 'Sea level pressure 10th percentile');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-PRES-90PCTL', 'Sea level pressure 90th percentile');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-PRES-NORMAL', 'Sea level pressure mean');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-TEMP-10PCTL', 'Temperature 10th percentile');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-TEMP-90PCTL', 'Temperature 90th percentile');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-TEMP-NORMAL', 'Temperature mean');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-WIND-1STDIR', 'Prevailing wind direction');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-WIND-1STPCT', 'Prevailing wind percentage');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-WIND-2NDDIR', 'Secondary wind direction');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-WIND-2NDPCT', 'Secondary wind percentage');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-WIND-AVGSPD', 'Average wind speed');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-WIND-PCTCLM', 'Percentage calm');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-WIND-VCTDIR', 'Mean wind vector direction');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-WIND-VCTSPD', 'Mean wind vector magnitude');
INSERT INTO data_type (data_type_id, descr) VALUES ('HLY-WCHL-NORMAL', 'Wind chill mean');

/*
 * Table containing weather station information.
 */
DROP TABLE IF EXISTS stations;
CREATE TABLE stations (
    code           CHAR(11) PRIMARY KEY NOT NULL,
    station_name   VARCHAR(128) NOT NULL,
    latitude       DECIMAL(9,6) NOT NULL,
    longitude      DECIMAL(9,6) NOT NULL,
    elevation      DECIMAL(9,6) NOT NULL
);

INSERT INTO stations (code, station_name, latitude, longitude, elevation) VALUES ('USW00023234', 'SAN FRANCISCO INTERNATIONAL AIRPORT, CA US', 37.619, -122.374, 2.4);
INSERT INTO stations (code, station_name, latitude, longitude, elevation) VALUES ('USW00023230', 'OAKLAND METROPOLITAN INTERNATIONAL AIRPORT, CA US', 37.721, -122.221, 3.4);
INSERT INTO stations (code, station_name, latitude, longitude, elevation) VALUES ('USW00023293', 'SAN JOSE INTERNATIONAL AIRPORT, CA US', 37.362, -121.929, 26.8);
INSERT INTO stations (code, station_name, latitude, longitude, elevation) VALUES ('USW00023213', 'SANTA ROSA SONOMA COUNTY AIRPORT, CA US', 38.508, -122.813, 36.6);
INSERT INTO stations (code, station_name, latitude, longitude, elevation) VALUES ('USW00023272', 'NAPA COUNTY AIRPORT, CA US', 38.213, -122.281, 2.4);
INSERT INTO stations (code, station_name, latitude, longitude, elevation) VALUES ('USW00023290', 'CONCORD BUCHANAN FIELD AIRPORT, CA US', 37.988, -122.058, 6.1);
INSERT INTO stations (code, station_name, latitude, longitude, elevation) VALUES ('USW00023244', 'HAYWARD AIR TERMINAL, CA US', 37.659, -122.121, 13.7);
INSERT INTO stations (code, station_name, latitude, longitude, elevation) VALUES ('USW00023234', 'SAN CARLOS AIRPORT, CA US', 37.511, -122.249, 1.5);
INSERT INTO stations (code, station_name, latitude, longitude, elevation) VALUES ('USW00094728', 'NEW YORK CITY, NY US', 40.7128, -74.0060, 2.4);
INSERT INTO stations (code, station_name, latitude, longitude, elevation) VALUES ('USW00014734', 'NEWARK, NJ US', 40.7357, -74.1724, 3.4);
INSERT INTO stations (code, station_name, latitude, longitude, elevation) VALUES ('USW00094789', 'JFK, NY US', 40.6413, -73.7781, 26.8);
INSERT INTO stations (code, station_name, latitude, longitude, elevation) VALUES ('USW00014732', 'WHITE PLAINS, NY US', 41.0339, -73.7629, 36.6);


/*
 * Table containing weather data comprised of hourly measurements by year.
 */
DROP TABLE IF EXISTS measurements;
CREATE TABLE measurements (
    id                SERIAL PRIMARY KEY,
    station_code      CHAR(11) NOT NULL,
    data_type_id      DataType NOT NULL,
    hour              CHAR(14) NOT NULL,
    year              INT NOT NULL,
    measurement       DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (station_code) REFERENCES stations(code),
    FOREIGN KEY (data_type_id) REFERENCES data_type(data_type_id)
);
