# Weather Prediction Application

Ứng dụng dự đoán thời tiết sử dụng mô hình học máy để dự đoán các chỉ số thời tiết như lượng mưa, xác suất bão, chỉ số UV, tầm nhìn, và thời tiết nắng.

---

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Cài đặt](#cài-đặt)
- [Chạy ứng dụng](#chạy-ứng-dụng)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
- [Mô hình học máy](#mô-hình-học-máy)
- [Tải mô hình đã huấn luyện](#tải-mô-hình-đã-huấn-luyện)
- [Liên hệ](#liên-hệ)

---

## Giới thiệu

Ứng dụng này sử dụng Flask làm framework backend và một mô hình học máy đa mục tiêu để dự đoán các chỉ số thời tiết dựa trên dữ liệu đầu vào. Các tính năng chính bao gồm:

- Dự đoán lượng mưa lớn hay không.
- Dự đoán xác suất bão.
- Dự đoán chỉ số UV (có hoặc không).
- Dự đoán tầm nhìn xa (km).
- Dự đoán thời tiết nắng.

---

## Cài đặt

### 1. Tạo môi trường ảo

```bash
python -m venv .venv
```

### 2. Kích hoạt môi trường ảo

- **Windows (Git Bash):**
  ```bash
  source .venv/Scripts/activate
  ```
- **Windows (Command Prompt):**
  ```cmd
  .venv\Scripts\activate
  ```
- **Linux/MacOS:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

---

## Chạy ứng dụng

### 1. Chạy ứng dụng Flask

```bash
python app.py
```

Ứng dụng sẽ chạy tại địa chỉ: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 2. Chạy giao diện MLflow (nếu cần)

```bash
mlflow ui
```

MLflow sẽ chạy tại địa chỉ: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Cấu trúc thư mục

```plaintext
.
├── app.py                  # File chính để chạy ứng dụng Flask
├── train.py                # File huấn luyện mô hình học máy
├── requirements.txt        # Danh sách các thư viện cần thiết
├── .env                    # File chứa các biến môi trường
├── controller/             # Chứa các controller xử lý logic
│   ├── index_controller.py
│   ├── predict_controller.py
│   ├── rainfall_controller.py
│   ├── storm_controller.py
│   ├── sunny_controller.py
│   ├── uv_controller.py
│   └── visibility_controller.py
├── routes/                 # Chứa các route Flask
│   ├── index_route.py
│   ├── predict_route.py
│   ├── rainfall_route.py
│   ├── storm_route.py
│   ├── sunny_route.py
│   ├── uv_route.py
│   └── visibility_route.py
├── templates/              # Chứa các file HTML
│   ├── index.html
│   ├── rainfall.html
│   ├── storm.html
│   ├── sunny.html
│   ├── uv.html
│   └── visibility.html
├── static/                 # Chứa các file CSS và JavaScript
│   ├── css/
│   └── js/
├── models/                 # Chứa các mô hình học máy đã huấn luyện
│   └── multi_target_model.pkl
├── data/                   # Chứa dữ liệu và kết quả tuning
│   ├── tuning_results.json
│   └── weather_data_with_targets.csv
└── notebooks/              # Chứa các notebook Jupyter (nếu có)
```

---

## Hướng dẫn sử dụng

### 1. Truy cập các trang dự đoán

- **Dự đoán lượng mưa:** [http://127.0.0.1:5000/rainfall](http://127.0.0.1:5000/rainfall)
- **Dự đoán xác suất bão:** [http://127.0.0.1:5000/storm](http://127.0.0.1:5000/storm)
- **Dự đoán chỉ số UV:** [http://127.0.0.1:5000/uv](http://127.0.0.1:5000/uv)
- **Dự đoán tầm nhìn:** [http://127.0.0.1:5000/visibility](http://127.0.0.1:5000/visibility)
- **Dự đoán thời tiết nắng:** [http://127.0.0.1:5000/sunny](http://127.0.0.1:5000/sunny)

### 2. Nhập thông tin thời tiết

- Nhấn nút "Thêm thông tin thời tiết" trên mỗi trang.
- Nhập các thông tin như nhiệt độ, độ ẩm, áp suất, tốc độ gió, mức độ mây.
- Nhấn "Dự đoán" để xem kết quả.

---

## Mô hình học máy

### 1. Mô hình sử dụng

- **RandomForestClassifier**: Mô hình học máy đa mục tiêu được sử dụng để dự đoán các chỉ số thời tiết.

### 2. Dữ liệu huấn luyện

- Dữ liệu được lưu trữ trong file `data/weather_data_with_targets.csv`.

### 3. Huấn luyện mô hình

- Chạy file `train.py` để huấn luyện mô hình:
  ```bash
  python train.py
  ```
- Mô hình tốt nhất sẽ được lưu trong thư mục `models/multi_target_model.pkl`.

---

## Tải mô hình đã huấn luyện

- https://drive.google.com/file/d/1c2AD4-WGZeheBYjAmcwFYpeNq3xaftV5/view?usp=sharing

---

## Liên hệ

Nếu bạn có bất kỳ câu hỏi nào, vui lòng liên hệ qua email: `support@weatherapp.com`.
