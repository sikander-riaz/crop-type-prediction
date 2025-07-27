from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from model.predict import predict_output, model, MODEL_VERSION
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
import pandas as pd

# ✅ First, create the app
app = FastAPI(title="Crop Prediction API", version="1.0.0")

# ✅ Then, add middleware to the already-created app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Human-readable check
@app.get('/')
def home():
    return {'message': 'Crop Prediction API'}

# ✅ Health check endpoint
@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }

# ✅ Crop prediction POST endpoint
@app.post("/predict", response_model=PredictionResponse)
def predict_crop(data: UserInput):
    """
    Predict crop type based on input features
    """
    user_input = {
        'N': data.N,
        'P': data.P,
        'K': data.K,
        'temperature': data.temperature,
        'humidity': data.humidity,
        'ph': data.ph,
        'rainfall': data.rainfall,
    }

    try:
        prediction = predict_output(user_input)
        return JSONResponse(status_code=200, content=prediction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
g