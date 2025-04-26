import time
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
import pandas as pd
import numpy as np
import os
import joblib
import json

experiment_name = "Weather_Prediction_Experiment"
mlflow.set_experiment(experiment_name)

# Sinh dữ liệu phân loại giả lập cho bài toán dự đoán thời tiết
X, y = make_classification( 
    n_samples=20000,  # Số lượng mẫu
    n_features=5,    # Số lượng đặc trưng (giả định: nhiệt độ, độ ẩm, áp suất, gió, mây)
    n_informative=4, # Số lượng đặc trưng quan trọng
    n_redundant=1,
    random_state=42
)

# Đặt tên cho các đặc trưng
columns = ["temperature", "humidity", "pressure", "wind", "clouds"]
X = pd.DataFrame(X, columns=columns)

# Sinh dữ liệu giả lập cho các chỉ số bổ sung
np.random.seed(42)
X["uv_index"] = np.random.uniform(0, 11, size=len(X))  # UV Index (0-11)
X["rainfall"] = np.random.uniform(0, 200, size=len(X))  # Lượng mưa (mm)
X["visibility"] = np.random.uniform(0, 10, size=len(X))  # Tầm nhìn xa (km)
X["storm_probability"] = np.random.uniform(0, 1, size=len(X))  # Xác suất xảy ra bão (0-1)
X["rain_probability"] = np.random.uniform(0, 1, size=len(X))  # Xác suất xảy ra mưa (0-1)

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)

# Các chỉ số cần dự đoán
targets = ["uv_index", "rainfall", "visibility", "storm_probability", "rain_probability"]

# Huấn luyện một mô hình duy nhất cho tất cả các chỉ số
y_train = X_train[targets]  # Tất cả các chỉ số mục tiêu
y_test = X_test[targets]
X_train_features = X_train[columns]
X_test_features = X_test[columns]

# Tạo mô hình hồi quy
model = RandomForestRegressor(n_estimators=100, max_depth=100, random_state=42)
model.fit(X_train_features, y_train)

# Dự đoán và tính các chỉ số đánh giá
preds = model.predict(X_test_features)
mse = mean_squared_error(y_test, preds, multioutput='raw_values')  # Tính MSE cho từng chỉ số
r2 = r2_score(y_test, preds, multioutput='raw_values')  # Tính R² cho từng chỉ số

# Log các chỉ số vào MLflow
for i, target in enumerate(targets):
    mlflow.log_metric(f"{target}_mse", mse[i])
    mlflow.log_metric(f"{target}_r2", r2[i])

# Thử nghiệm tuning hyperparameters
max_depth_values = [10, 15, 20, 25, 30, None]
n_estimators_values = [100, 150, 200, 300, 500, 1000]

best_accuracy = -np.inf
best_model = None

# Lưu kết quả tuning
tuning_results = []

for max_depth in max_depth_values:
    for n_estimators in n_estimators_values:
        # Kết thúc run trước đó nếu còn tồn tại
        if mlflow.active_run() is not None:
            print(f"Kết thúc run hiện tại: {mlflow.active_run().info.run_id}")
            mlflow.end_run()

        with mlflow.start_run() as run:
            # Tạo mô hình với siêu tham số
            model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
            model.fit(X_train_features, y_train)

            # Dự đoán và tính các chỉ số đánh giá
            preds = model.predict(X_test_features)
            mse = mean_squared_error(y_test, preds, multioutput='raw_values')  # Tính MSE cho từng chỉ số
            r2 = r2_score(y_test, preds, multioutput='raw_values')  # Tính R² cho từng chỉ số

            # Log siêu tham số và chỉ số
            mlflow.log_param("max_depth", max_depth)
            mlflow.log_param("n_estimators", n_estimators)
            for i, target in enumerate(targets):
                mlflow.log_metric(f"{target}_mse", mse[i])
                mlflow.log_metric(f"{target}_r2", r2[i])

            # Lưu kết quả tuning
            tuning_results.append({
                "max_depth": max_depth,
                "n_estimators": n_estimators,
                "avg_r2": np.mean(r2),
                "mse": mse.tolist(),
                "r2": r2.tolist()
            })

            # Cập nhật mô hình tốt nhất dựa trên trung bình R²
            avg_r2 = np.mean(r2)  # Tính trung bình R² cho tất cả các chỉ số
            if avg_r2 > best_accuracy:
                best_accuracy = avg_r2
                best_model = model

# Lưu mô hình tốt nhất
os.makedirs("models", exist_ok=True)
joblib.dump(best_model, "models/multi_target_model.pkl")
print("Mô hình dự đoán nhiều chỉ số tốt nhất đã được lưu vào models/multi_target_model.pkl")

mlflow.sklearn.log_model(best_model, artifact_path="model")
print("Mô hình tốt nhất đã được lưu vào MLflow.")
# Lưu kết quả tuning vào file JSON
with open("data/tuning_results.json", "w") as f:
    json.dump(tuning_results, f)
print("Kết quả tuning đã được lưu vào data/tuning_results.json")