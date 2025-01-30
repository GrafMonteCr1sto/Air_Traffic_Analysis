-- Удаление существующих таблиц в правильном порядке (из-за foreign key constraints)
DROP TABLE IF EXISTS ticket_prices;
DROP TABLE IF EXISTS economic_indicators;
DROP TABLE IF EXISTS weather;
DROP TABLE IF EXISTS passengers;
DROP TABLE IF EXISTS flights;
DROP TABLE IF EXISTS airports;

-- Таблица аэропортов
CREATE TABLE airports (
    airport_code VARCHAR(10) PRIMARY KEY,
    city VARCHAR(100),
    country VARCHAR(100)
);

-- Таблица рейсов
CREATE TABLE flights (
    flight_id INT PRIMARY KEY AUTO_INCREMENT,
    departure_airport VARCHAR(10),
    arrival_airport VARCHAR(10),
    flight_date DATE,
    passengers_count INT,
    FOREIGN KEY (departure_airport) REFERENCES airports(airport_code),
    FOREIGN KEY (arrival_airport) REFERENCES airports(airport_code)
);

-- Таблица пассажиров
CREATE TABLE passengers (
    passenger_id INT PRIMARY KEY AUTO_INCREMENT,
    flight_id INT,
    age INT,
    gender ENUM('M', 'F'),
    class ENUM('Economy', 'Business', 'First'),
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id)
);

-- Таблица погодных условий
CREATE TABLE weather (
    date DATE,
    airport_code VARCHAR(10),
    temperature FLOAT,
    holiday BOOLEAN,
    weekday INT,
    PRIMARY KEY (date, airport_code),
    FOREIGN KEY (airport_code) REFERENCES airports(airport_code)
);

-- Таблица экономических показателей
CREATE TABLE economic_indicators (
    date DATE PRIMARY KEY,
    gdp FLOAT,
    inflation FLOAT
);

-- Таблица цен на билеты
CREATE TABLE ticket_prices (
    flight_id INT,
    avg_ticket_price FLOAT,
    PRIMARY KEY (flight_id),
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id)
);

-- Генерация тестовых данных
INSERT INTO airports (airport_code, city, country) VALUES
('SVO', 'Moscow', 'Russia'),
('JFK', 'New York', 'USA'),
('DME', 'Moscow', 'Russia'),
('CDG', 'Paris', 'France'),
('LHR', 'London', 'UK'),
('FRA', 'Frankfurt', 'Germany'),
('LED', 'Saint Petersburg', 'Russia'),
('SEA', 'Seattle', 'USA'),
('HND', 'Tokyo', 'Japan'),
('SYD', 'Sydney', 'Australia'),
('DXB', 'Dubai', 'UAE'),
('AMS', 'Amsterdam', 'Netherlands'),
('LAX', 'Los Angeles', 'USA'),
('BKK', 'Bangkok', 'Thailand'),
('IST', 'Istanbul', 'Turkey'),
('PEK', 'Beijing', 'China'),
('HKG', 'Hong Kong', 'China'),
('SIN', 'Singapore', 'Singapore'),
('ICN', 'Seoul', 'South Korea'),
('MEX', 'Mexico City', 'Mexico');

-- Добавляем больше рейсов
INSERT INTO flights (departure_airport, arrival_airport, flight_date, passengers_count) VALUES
('SVO', 'JFK', '2024-01-10', 200),
('DME', 'CDG', '2024-01-10', 150),
('SVO', 'LHR', '2024-01-11', 180),
('DME', 'FRA', '2024-01-12', 120),
('LED', 'JFK', '2024-01-13', 100),
('SVO', 'SEA', '2024-02-01', 220),
('SVO', 'HND', '2024-02-02', 210),
('DME', 'SYD', '2024-02-03', 160),
('SVO', 'DXB', '2024-02-04', 250),
('LED', 'AMS', '2024-02-05', 200),
('CDG', 'LAX', '2024-02-06', 180),
('JFK', 'BKK', '2024-02-07', 170),
('IST', 'PEK', '2024-02-08', 190),
('HKG', 'SIN', '2024-02-09', 210),
('ICN', 'MEX', '2024-02-10', 230),
('PEK', 'HKG', '2024-02-11', 240),
('SIN', 'ICN', '2024-02-12', 220),
('MEX', 'IST', '2024-02-13', 200);

-- Добавляем больше пассажиров
INSERT INTO passengers (flight_id, age, gender, class) VALUES
(1, 32, 'M', 'Economy'),
(1, 27, 'F', 'Business'),
(2, 45, 'M', 'Economy'),
(2, 29, 'F', 'First'),
(3, 37, 'M', 'Economy'),
(6, 30, 'M', 'Economy'),
(6, 28, 'F', 'Business'),
(6, 35, 'M', 'First'),
(7, 42, 'F', 'Economy'),
(7, 38, 'M', 'Business'),
(8, 33, 'F', 'Economy'),
(8, 31, 'M', 'First'),
(9, 29, 'F', 'Economy'),
(9, 26, 'M', 'Business'),
(10, 36, 'M', 'Economy'),
(10, 33, 'F', 'First'),
(11, 41, 'M', 'Economy'),
(11, 40, 'F', 'Business'),
(12, 25, 'F', 'Economy'),
(12, 29, 'M', 'Business'),
(13, 34, 'M', 'Economy'),
(13, 31, 'F', 'Business'),
(14, 28, 'F', 'Economy'),
(14, 30, 'M', 'First'),
(15, 35, 'M', 'Economy'),
(15, 32, 'F', 'Business'),
(16, 29, 'F', 'Economy'),
(16, 27, 'M', 'First'),
(17, 33, 'M', 'Economy'),
(17, 30, 'F', 'Business'),
(18, 31, 'F', 'Economy'),
(18, 29, 'M', 'First');

-- Добавляем больше погодных данных
INSERT INTO weather (date, airport_code, temperature, holiday, weekday) VALUES
('2024-01-10', 'SVO', -5.0, FALSE, 3),
('2024-01-10', 'JFK', 2.0, FALSE, 3),
('2024-01-10', 'DME', -3.0, FALSE, 3),
('2024-01-10', 'CDG', 7.0, FALSE, 3),
('2024-01-10', 'LHR', 6.0, FALSE, 3),
('2024-01-10', 'FRA', 5.0, FALSE, 3),
('2024-01-10', 'LED', -2.0, FALSE, 3),
('2024-02-01', 'SVO', -6.0, FALSE, 4),
('2024-02-01', 'SEA', 8.0, FALSE, 4),
('2024-02-01', 'HND', 10.0, FALSE, 4),
('2024-02-02', 'DME', -4.0, FALSE, 5),
('2024-02-02', 'SYD', 22.0, TRUE, 5),
('2024-02-02', 'SVO', -7.0, FALSE, 5),
('2024-02-03', 'DXB', 28.0, FALSE, 6),
('2024-02-03', 'LED', -3.0, TRUE, 6),
('2024-02-03', 'AMS', 4.0, FALSE, 6),
('2024-02-04', 'CDG', 5.0, FALSE, 7),
('2024-02-04', 'LAX', 15.0, TRUE, 7),
('2024-02-05', 'JFK', 3.0, FALSE, 1),
('2024-02-05', 'BKK', 30.0, FALSE, 1),
('2024-02-06', 'IST', 12.0, FALSE, 2),
('2024-02-06', 'PEK', -1.0, FALSE, 2),
('2024-02-07', 'HKG', 18.0, FALSE, 3),
('2024-02-07', 'SIN', 28.0, FALSE, 3),
('2024-02-08', 'ICN', 5.0, FALSE, 4),
('2024-02-08', 'MEX', 20.0, FALSE, 4),
('2024-02-09', 'PEK', -2.0, FALSE, 5),
('2024-02-09', 'HKG', 19.0, FALSE, 5),
('2024-02-10', 'SIN', 27.0, FALSE, 6),
('2024-02-10', 'ICN', 6.0, FALSE, 6),
('2024-02-11', 'MEX', 21.0, FALSE, 7),
('2024-02-11', 'IST', 13.0, FALSE, 7);

-- Добавляем больше экономических показателей
INSERT INTO economic_indicators (date, gdp, inflation) VALUES
('2024-02-01', 1.9, 2.4),
('2024-02-02', 1.87, 2.6),
('2024-02-03', 1.92, 2.5),
('2024-02-04', 1.94, 2.3),
('2024-02-05', 1.90, 2.2),
('2024-02-06', 1.91, 2.1),
('2024-02-07', 1.93, 2.0),
('2024-02-08', 1.95, 1.9),
('2024-02-09', 1.96, 1.8),
('2024-02-10', 1.97, 1.7),
('2024-02-11', 1.98, 1.6);

-- Добавляем больше цен на билеты
INSERT INTO ticket_prices (flight_id, avg_ticket_price) VALUES
(1, 450.00),
(2, 380.00),
(3, 410.00),
(4, 350.00),
(5, 500.00),
(6, 470.00),
(7, 490.00),
(8, 460.00),
(9, 440.00),
(10, 520.00),
(11, 480.00),
(12, 510.00),
(13, 530.00),
(14, 540.00),
(15, 550.00),
(16, 560.00),
(17, 570.00),
(18, 580.00);