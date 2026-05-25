from flask import Blueprint, request, jsonify
from backend.services.model_service import predict_image

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]

        result = predict_image(file)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500