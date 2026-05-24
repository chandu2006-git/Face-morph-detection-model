from flask import Flask
from flask_cors import CORS
from backend.routes.predict import predict_bp

app = Flask(__name__)

# 🔥 VERY IMPORTANT — PLACE HERE (TOP)
CORS(app, resources={r"/*": {"origins": "*"}})

# Register routes AFTER CORS
app.register_blueprint(predict_bp)

@app.route("/")
def home():
    return "API Running ✅"