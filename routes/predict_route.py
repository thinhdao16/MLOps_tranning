from flask import Blueprint, request, jsonify
from controller.predict_controller import predict_logic

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict():
    try:
        features = request.form.get('features')
        result = predict_logic(features)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500