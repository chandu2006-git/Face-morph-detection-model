from flask import Flask, render_template
from backend.routes.predict import predict_bp
from flask_cors import CORS

app = Flask(__name__, 
            template_folder="../templates", 
            static_folder="../static")

CORS(app)

# Register API
app.register_blueprint(predict_bp)

@app.route('/')
def home():
    return "MorphGuard API is running 🚀"