from flask import Flask
from flask_cors import CORS
from backend.routes.predict import predict_bp
import os

# ✅ CREATE APP FIRST
app = Flask(__name__)

# ✅ ENABLE CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# ✅ REGISTER ROUTES
app.register_blueprint(predict_bp)

@app.route("/")
def home():
    return "API Running ✅"

# ✅ RUN SERVER (LAST)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)