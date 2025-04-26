from flask import Blueprint, request, render_template
from controller.predict_controller import predict_logic

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict():
    try:
        # Lấy dữ liệu từ form
        temperature = request.form.get('temperature')
        humidity = request.form.get('humidity')
        pressure = request.form.get('pressure')
        wind = request.form.get('wind')
        clouds = request.form.get('clouds')

        # Tạo chuỗi đầu vào cho mô hình
        features = f"{temperature},{humidity},{pressure},{wind},{clouds}"

        # Gọi hàm dự đoán
        result = predict_logic(features)

        # Trả về trang index.html với kết quả dự đoán
        return render_template('index.html', result=result)
    except Exception as e:
        return render_template('index.html', result={"error": str(e)})