import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, r2_score

# Загрузка данных
df = pd.read_csv("flights_data.csv")

# Преобразование даты и установка индекса
df["flight_date"] = pd.to_datetime(df["flight_date"])
df.set_index("flight_date", inplace=True)

# Заполнение пропусков
df = df.ffill().bfill()

# Преобразуем ТОЛЬКО категориальные признаки (города, holiday, weekday)
df = pd.get_dummies(df, columns=[
    "departure_city",
    "arrival_city",
    "holiday",
    "weekday"
])

# Разделение данных
X = df.drop(columns=["passengers_count"])
y = df["passengers_count"]

# Проверка типов данных (должны быть только числа)
print("Типы данных после преобразования:")
print(X.dtypes)

# Разделение на тренировочные и тестовые данные
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=False
)

# Масштабирование данных
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Обучение моделей
def train_ml_model(model, model_name):
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"{model_name} MAE: {mae:.2f}, R²: {r2:.2f}")
    return y_pred

xgb_model = XGBRegressor(n_estimators=150, learning_rate=0.05, random_state=42)
y_pred_xgb = train_ml_model(xgb_model, "XGBoost")

lgb_model = LGBMRegressor(n_estimators=150, learning_rate=0.05, random_state=42)
y_pred_lgb = train_ml_model(lgb_model, "LightGBM")

# Временные модели (ARIMA, SARIMA, Prophet) остаются без изменений
# ...

# Визуализация
plt.figure(figsize=(14, 7))
plt.plot(y_test.index, y_test, label="Фактические значения", color="black")
plt.scatter(y_test.index, y_pred_xgb, alpha=0.5, label="XGBoost")
plt.scatter(y_test.index, y_pred_lgb, alpha=0.5, label="LightGBM")
plt.legend()
plt.show()