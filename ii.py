from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np
from test import create_rd

# Создаем модель IsolationForest
model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)

# Задаем параметры нормализации данных
scaler = StandardScaler()

def detect_dos_attack(X):
    
    # Функция для обнаружения DoS атак на основе машинного обучения.
    # Принимает на вход массив признаков X, который содержит данные о сетевом трафике.
    # Если модель определяет, что входные данные указывают на DoS атаку, функция возвращает True, иначе - False.
    
    # Нормализуем данные
    X_scaled = scaler.fit_transform(X)
    # Обучаем модель
    model.fit(X_scaled)
    # Предсказываем метки аномальности для входных данных
    y_pred = model.predict(X_scaled)
    # Если среди предсказанных меток есть аномальные данные, возвращаем True (есть DoS атака), иначе - False (нет DoS атаки)
    return -1 in y_pred

print(detect_dos_attack(create_rd(10,200)))