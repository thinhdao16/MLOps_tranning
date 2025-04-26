from flask import Blueprint, render_template, request
from controller.predict_controller import predict_logic
from utils.openweather import fetch_weather_data

visibility_bp = Blueprint('visibility', __name__)

user_data_list = []

@visibility_bp.route('/visibility', methods=['GET', 'POST'])
def visibility():
    cities = ["Ho Chi Minh", "Hanoi", "Da Nang", "Can Tho", "Hải Phòng", "Nha Trang", "Vinh"]
    weather_data_list = []

    # Lấy dữ liệu thời tiết từ OpenWeatherMap cho các thành phố
    for city_name in cities:
        weather_data = fetch_weather_data(city_name)
        if "error" in weather_data:
            weather_data_list.append({"city": city_name, "error": weather_data["error"]})
            continue

        features = {
            "temperature": weather_data.get("main", {}).get("temp", 0),
            "humidity": weather_data.get("main", {}).get("humidity", 0),
            "pressure": weather_data.get("main", {}).get("pressure", 0),
            "wind": weather_data.get("wind", {}).get("speed", 0),
            "clouds": weather_data.get("clouds", {}).get("all", 0),
        }

        features_str = f"{features['temperature']},{features['humidity']},{features['pressure']},{features['wind']},{features['clouds']}"
        prediction = predict_logic(features_str)

        formatted_prediction = {
            "visibility": "Có" if prediction["visibility"] == 1 else "Không",
        }

        weather_data_list.append({
            "city": city_name,
            "weather": weather_data,
            "prediction": formatted_prediction
        })

    # Xử lý dữ liệu từ form người dùng
    if request.method == 'POST':
        name = request.form.get('name', 'Người dùng không tên')
        temperature = float(request.form.get('temperature', 0))
        humidity = float(request.form.get('humidity', 0))
        pressure = float(request.form.get('pressure', 0))
        wind = float(request.form.get('wind', 0))
        clouds = float(request.form.get('clouds', 0))

        user_features_str = f"{temperature},{humidity},{pressure},{wind},{clouds}"
        user_prediction = predict_logic(user_features_str)

        user_data = {
            "city": name,
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure,
            "wind": wind,
            "clouds": clouds,
            "visibility": "Có" if user_prediction["visibility"] == 1 else "Không",
        }
        user_data_list.append(user_data)

    return render_template('visibility.html', weather_data_list=weather_data_list, user_data_list=user_data_list)