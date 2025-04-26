from flask import Flask
from routes import register_routes

app = Flask(__name__)

# Đăng ký tất cả các route từ routes/
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)