from flask import Blueprint, render_template
from controller.index_controller import get_weather_for_homepage

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    # Lấy dữ liệu thời tiết cho trang chủ
    weather_data = get_weather_for_homepage()
    print("Dữ liệu thời tiết:", weather_data)
    return render_template('index.html', weather_data=weather_data)