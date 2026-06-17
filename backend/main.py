from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from backend.model_service import predict_image

app = FastAPI(title="MorphGuard API")

origins = [
    "https://face-morph-detection-model-5iu1.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "status": "running",
        "model": "InceptionV3"
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    result = predict_image(file.file)

    return result