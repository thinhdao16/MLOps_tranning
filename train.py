# filepath: train.py
import time
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np

# Đặt tên cho experiment
experiment_name = "Mlflow_Classification_Experiment"
mlflow.set_experiment(experiment_name)

# Sinh dữ liệu phân loại giả sử
X, y = make_classification(n_samples=5000, n_features=20, n_informative=15, n_redundant=5, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

best_accuracy = -np.inf
best_run_id = None

# Thử nghiệm tuning hyperparameters
max_depth_values = [None, 3, 5, 7]
min_samples_split_values = [2, 5, 10]
min_samples_leaf_values = [1, 2, 4]
criterion_values = ["gini", "entropy"]
alpha_values = [0.1, 0.5, 1.0]  # Thêm alpha làm ví dụ

for max_depth in max_depth_values:
    for min_samples_split in min_samples_split_values:
        for min_samples_leaf in min_samples_leaf_values:
            for criterion in criterion_values:
                for alpha in alpha_values:
                    start_time = time.time()  # Bắt đầu đo thời gian
                    with mlflow.start_run() as run:
                        # Log các siêu tham số
                        mlflow.log_param("max_depth", max_depth)
                        mlflow.log_param("min_samples_split", min_samples_split)
                        mlflow.log_param("min_samples_leaf", min_samples_leaf)
                        mlflow.log_param("criterion", criterion)
                        mlflow.log_param("alpha", alpha)

                        # Tạo mô hình Random Forest
                        model = RandomForestClassifier(
                            n_estimators=100,
                            max_depth=max_depth,
                            min_samples_split=min_samples_split,
                            min_samples_leaf=min_samples_leaf,
                            criterion=criterion,
                            random_state=42
                        )
                        model.fit(X_train, y_train)

                        # Dự đoán và tính các metric
                        preds = model.predict(X_test)
                        acc = accuracy_score(y_test, preds)
                        precision = precision_score(y_test, preds)
                        recall = recall_score(y_test, preds)
                        f1 = f1_score(y_test, preds)

                        # Log các metric
                        mlflow.log_metric("accuracy", acc)
                        mlflow.log_metric("precision", precision)
                        mlflow.log_metric("recall", recall)
                        mlflow.log_metric("f1_score", f1)

                        # Log thời gian chạy
                        duration = time.time() - start_time
                        mlflow.log_metric("duration", duration)

                        # Log model
                        mlflow.sklearn.log_model(model, "model")

                        # In ra kết quả cho lần chạy này
                        print(f"Run {run.info.run_id} với max_depth={max_depth}, min_samples_split={min_samples_split}, "
                              f"min_samples_leaf={min_samples_leaf}, criterion={criterion}, alpha={alpha} đạt "
                              f"accuracy: {acc}, precision: {precision}, recall: {recall}, f1_score: {f1}, duration: {duration:.2f}s")

                        # Cập nhật mô hình tốt nhất nếu accuracy cao hơn
                        if acc > best_accuracy:
                            best_accuracy = acc
                            best_run_id = run.info.run_id

print(f"Best run ID: {best_run_id} với accuracy: {best_accuracy}")

# Đăng ký mô hình tốt nhất vào Model Registry
client = MlflowClient()
model_uri = f"runs:/{best_run_id}/model"
model_name = "BestModelClassification"

# Đăng ký mô hình (nếu đã tồn tại, phiên bản mới sẽ được tạo)
result = mlflow.register_model(model_uri, model_name)
print(f"Registered model version: {result.version}")

# Chuyển trạng thái mô hình sang 'Production'
client.transition_model_version_stage(
    name=model_name,
    version=result.version,
    stage="Production",
    archive_existing_versions=True
)
print(f"Mô hình {model_name} version {result.version} đã được chuyển sang Production stage.")