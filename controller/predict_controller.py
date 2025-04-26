import joblib
import pandas as pd

# Tải mô hình từ thư mục models/
model = joblib.load("models/multi_target_model.pkl")
print("Mô hình đã được tải từ models/multi_target_model.pkl")

def predict_logic(features):
    # Chuyển đổi chuỗi đầu vào thành danh sách số thực
    features = [float(x) for x in features.split(',')]

    # Nếu là một mẫu đơn, chuyển thành mảng 2 chiều
    if isinstance(features[0], (int, float)):
        features = [features]

    # Chuyển đổi thành DataFrame với tên cột
    columns = ["temperature", "humidity", "pressure", "wind", "clouds"]
    features_df = pd.DataFrame(features, columns=columns)

    # Dự đoán
    predictions = model.predict(features_df)[0]  # Lấy kết quả dự đoán cho mẫu đầu tiên

    # Trả về kết quả dưới dạng dictionary
    result = {target: predictions[i] for i, target in enumerate(["uv_index", "rainfall", "visibility", "storm_probability", "rain_probability"])}
    return result