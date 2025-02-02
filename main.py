import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from prophet import Prophet


warnings.filterwarnings("ignore")
df = pd.read_csv("flights_data.csv")

df["flight_date"] = pd.to_datetime(df["flight_date"])
df = df.sort_values("flight_date")
df.set_index("flight_date", inplace=True)
print("Количество пропусков по столбцам:")
print(df.isnull().sum())

df = df.ffill().bfill()
df["passengers_7d_avg"] = df["passengers_count"].rolling(window=7, min_periods=1).mean()

# ====================================
# 2. Корреляционный анализ
# ====================================
numeric_df = df.select_dtypes(include=[np.number])
plt.figure(figsize=(12, 8))
sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Корреляционная матрица числовых признаков")
plt.show()

# ====================================
# 3. Инженерия признаков для моделирования
# ====================================
categorical_cols = ["departure_city", "arrival_city", "holiday", "weekday"]
df_model = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# ====================================
# 4. Подготовка данных для обучения моделей
# ====================================
X = df_model.drop(columns=["passengers_count"])
y = df_model["passengers_count"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

train_size = int(len(X_scaled) * 0.8)
X_train, X_test = X_scaled[:train_size], X_scaled[train_size:]
y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]

print("Размер тренировочной выборки:", X_train.shape)
print("Размер тестовой выборки:", X_test.shape)

# ====================================
# 5. Обучение моделей машинного обучения
# ====================================
def evaluate_model(model, name):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"{name} -> MAE: {mae:.2f}, R²: {r2:.2f}")
    return y_pred


xgb_model = XGBRegressor(n_estimators=150, learning_rate=0.05, random_state=42)
y_pred_xgb = evaluate_model(xgb_model, "XGBoost")

lgb_model = LGBMRegressor(n_estimators=150, learning_rate=0.05, random_state=42)
y_pred_lgb = evaluate_model(lgb_model, "LightGBM")

cat_model = CatBoostRegressor(iterations=150, learning_rate=0.05, random_state=42, verbose=0)
y_pred_cat = evaluate_model(cat_model, "CatBoost")

# ====================================
# 6. Временной ряд: прогнозирование с Prophet
# ====================================
df_prophet = df.reset_index()[["flight_date", "passengers_count", "temperature", "gdp", "inflation", "avg_ticket_price"]]
df_prophet.rename(columns={"flight_date": "ds", "passengers_count": "y"}, inplace=True)


prophet_model = Prophet(daily_seasonality=True)
prophet_model.add_regressor("temperature")
prophet_model.add_regressor("gdp")
prophet_model.add_regressor("inflation")
prophet_model.add_regressor("avg_ticket_price")

prophet_model.fit(df_prophet)

future = prophet_model.make_future_dataframe(periods=30)
last_row = df_prophet.iloc[-1]
future["temperature"] = last_row["temperature"]
future["gdp"] = last_row["gdp"]
future["inflation"] = last_row["inflation"]
future["avg_ticket_price"] = last_row["avg_ticket_price"]

forecast_prophet = prophet_model.predict(future)

# ====================================
# 7. Визуализация результатов
# ====================================
plt.figure(figsize=(14, 7))
plt.plot(y_test.index, y_test, label="Фактические значения", color="black", linewidth=2)
plt.plot(y_test.index, y_pred_xgb, label="XGBoost", linestyle="--")
plt.plot(y_test.index, y_pred_lgb, label="LightGBM", linestyle="--")
plt.plot(y_test.index, y_pred_cat, label="CatBoost", linestyle="--")
plt.xlabel("Дата")
plt.ylabel("Количество пассажиров")
plt.title("Сравнение предсказаний ML моделей")
plt.legend()
plt.grid(True)
plt.show()

fig1 = prophet_model.plot(forecast_prophet)
plt.title("Прогноз пассажиропотока с Prophet")
plt.xlabel("Дата")
plt.ylabel("Пассажиры")
plt.show()

fig2 = prophet_model.plot_components(forecast_prophet)
plt.show()

print("Анализ завершен.")