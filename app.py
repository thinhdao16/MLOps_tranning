# filepath: app.py
from flask import Flask, request, jsonify, render_template
import mlflow.pyfunc
import numpy as np

app = Flask(__name__)

# Tải mô hình từ Model Registry với stage Production
model_name = "BestModelClassification"
model = mlflow.pyfunc.load_model(f"models:/{model_name}/Production")
print(f"Loaded model {model_name} từ Production stage.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Lấy dữ liệu từ form
        features = request.form.get('features')
        features = [float(x) for x in features.split(',')]
        
        # Nếu là một mẫu đơn, chuyển thành mảng 2 chiều
        if isinstance(features[0], (int, float)):
            features = [features]
        
        # Kiểm tra số lượng tính năng mỗi mẫu, dự kiến cần có 20 tính năng
        expected_features = 20
        for idx, sample in enumerate(features):
            if len(sample) != expected_features:
                return jsonify({"error": f"Sample {idx} có {len(sample)} features, nhưng dự kiến cần {expected_features} features."}), 400
        
        # Dự đoán
        predictions = model.predict(features)
        return jsonify({"predictions": predictions.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)