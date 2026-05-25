from flask import Flask
from flask_cors import CORS
from backend.routes.predict import predict_bp

app = Flask(__name__)

# 🔥 CORS FIX
CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(predict_bp)


@app.route("/")
def home():
    return "API Running ✅"