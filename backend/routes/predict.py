from flask import Blueprint, request, jsonify
from backend.services.model_service import predict_image

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    try:
        print("📥 Request received")

        if "file" not in request.files:
            print("❌ No file in request")
            return jsonify({"error": "No file"}), 400

        file = request.files["file"]
        print("📂 File received:", file.filename)

        result = predict_image(file)

        print("✅ Prediction done:", result)

        return jsonify(result)

    except Exception as e:
        print("🔥 CRASH ERROR:", str(e))   # 🔥 THIS IS KEY
        return jsonify({"error": str(e)}), 500