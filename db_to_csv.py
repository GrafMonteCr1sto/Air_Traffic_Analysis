import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:Niksql_1@localhost/air_traffic')

# Убираем departure_airport и arrival_airport, так как используем города
query = """
SELECT 
    f.flight_date,
    f.passengers_count,
    a1.city as departure_city,
    a2.city as arrival_city,
    w.temperature,
    w.holiday,
    w.weekday,
    e.gdp,
    e.inflation,
    tp.avg_ticket_price
FROM flights f
LEFT JOIN airports a1 ON f.departure_airport = a1.airport_code
LEFT JOIN airports a2 ON f.arrival_airport = a2.airport_code
LEFT JOIN weather w ON f.flight_date = w.date AND f.departure_airport = w.airport_code
LEFT JOIN economic_indicators e ON DATE(f.flight_date) = e.date
LEFT JOIN ticket_prices tp ON f.flight_id = tp.flight_id
"""

try:
    df = pd.read_sql(query, engine)
    df.to_csv('flights_data.csv', index=False)
    print("Данные сохранены в flights_data.csv")
except Exception as e:
    print(f"Ошибка: {e}")