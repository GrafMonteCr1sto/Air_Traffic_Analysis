from sqlalchemy import create_engine, text

# Подключение к MySQL
engine = create_engine("mysql+pymysql://root:Niksql_1@localhost")

# Создание базы данных, если её нет
with engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS air_traffic;"))
    conn.commit()

# Подключение к базе
engine = create_engine("mysql+pymysql://root:Niksql_1@localhost/air_traffic")

# Читаем SQL-скрипт и выполняем его построчно
with engine.connect() as conn:
    with open("script.sql", "r", encoding="utf-8") as file:
        sql_script = file.read()

    # Разбиваем SQL-файл по `;` и выполняем команды отдельно
    for statement in sql_script.split(";"):
        statement = statement.strip()
        if statement:  # Игнорируем пустые строки
            conn.execute(text(statement))
            conn.commit()

print("База данных и таблицы успешно созданы!")