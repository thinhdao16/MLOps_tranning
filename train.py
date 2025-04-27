import time
import mlflow
import mlflow.sklearn
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import os
import joblib
import json

# Đặt tên cho experiment trong MLflow
experiment_name = "Weather_Prediction_Experiment"
mlflow.set_experiment(experiment_name)

# Sinh dữ liệu phân loại giả lập với make_classification
X, y = make_classification(
    n_samples=100000,  # Số lượng mẫu
    n_features=5,     # Số lượng đặc trưng (giả định: nhiệt độ, độ ẩm, áp suất, gió, mây)
    n_informative=4,  # Số lượng đặc trưng quan trọng
    n_redundant=1,
    random_state=42
)

# Đặt tên cho các đặc trưng (ví dụ: nhiệt độ, độ ẩm...)
columns = ["temperature", "humidity", "pressure", "wind", "clouds"]
X = pd.DataFrame(X, columns=columns)

# Sinh dữ liệu giả lập cho các chỉ số thời tiết
np.random.seed(42)
X["uv_index"] = np.random.uniform(0, 11, size=len(X))  # UV Index (0-11)
X["rainfall"] = np.random.uniform(0, 200, size=len(X))  # Lượng mưa (mm)
X["visibility"] = np.random.uniform(0, 10, size=len(X))  # Tầm nhìn xa (km)
X["storm_probability"] = np.random.uniform(0, 1, size=len(X))  # Xác suất xảy ra bão (0-1)
X["rain_probability"] = np.random.uniform(0, 1, size=len(X))  # Xác suất xảy ra mưa (0-1)

# Biến y: Phân loại thành 2 lớp (0: thấp, 1: cao) cho các chỉ số
y_multi = pd.DataFrame({
    "uv_index": (X["uv_index"] > 5).astype(int),  # 0: UV thấp, 1: UV cao
    "rainfall": (X["rainfall"] > 50).astype(int),  # 0: ít mưa, 1: mưa nhiều
    "visibility": (X["visibility"] < 5).astype(int),  # 0: tầm nhìn xa, 1: tầm nhìn gần
    "storm_probability": (X["storm_probability"] > 0.5).astype(int),  # 0: không bão, 1: có bão
    "rain_probability": (X["rain_probability"] > 0.5).astype(int)  # 0: không mưa, 1: mưa
})

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X[columns], y_multi, test_size=0.2, random_state=42)

# Tuning siêu tham số
max_depth_values = [5, 10, 15, 20, 25]  # Thêm nhiều giá trị hơn cho max_depth
n_estimators_values = [50, 100, 150, 200, 250]  # Thêm nhiều giá trị hơn cho n_estimators

best_accuracy = -np.inf
best_model = None

# Lưu kết quả tuning
tuning_results = []

for max_depth in max_depth_values:
    for n_estimators in n_estimators_values:
        # Kết thúc run trước đó nếu còn tồn tại
        if mlflow.active_run() is not None:
            mlflow.end_run()

        with mlflow.start_run() as run:
            # Tạo mô hình đa mục tiêu với siêu tham số
            base_model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
            multi_target_model = MultiOutputClassifier(base_model)
            multi_target_model.fit(X_train, y_train)

            # Dự đoán và tính độ chính xác trung bình
            y_pred = multi_target_model.predict(X_test)
            accuracies = []
            for i, label in enumerate(y_multi.columns):
                accuracy = accuracy_score(y_test.iloc[:, i], y_pred[:, i])
                accuracies.append(accuracy)
                mlflow.log_metric(f"accuracy_{label}", accuracy)

            avg_accuracy = np.mean(accuracies)
            mlflow.log_param("max_depth", max_depth)
            mlflow.log_param("n_estimators", n_estimators)
            mlflow.log_metric("avg_accuracy", avg_accuracy)

            # Lưu kết quả tuning
            tuning_results.append({
                "max_depth": max_depth,
                "n_estimators": n_estimators,
                "avg_accuracy": avg_accuracy
            })

            # Cập nhật mô hình tốt nhất
            if avg_accuracy > best_accuracy:
                best_accuracy = avg_accuracy
                best_model = multi_target_model

# Lưu mô hình tốt nhất
os.makedirs("models", exist_ok=True)
joblib.dump(best_model, "models/multi_target_model.pkl")
print("Mô hình đa mục tiêu tốt nhất đã được lưu vào models/multi_target_model.pkl")

mlflow.sklearn.log_model(best_model, artifact_path="model")
print("Mô hình đa mục tiêu tốt nhất đã được lưu vào MLflow.")

# Lưu kết quả tuning vào file JSON
os.makedirs("data", exist_ok=True)
with open("data/tuning_results.json", "w") as f:
    json.dump(tuning_results, f)
print("Kết quả tuning đã được lưu vào data/tuning_results.json")
