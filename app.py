import logging
import pickle

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from model.predict import predict_output, model, MODEL_VERSION

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model
try:
    with open('model/model.pkl', 'rb') as f:
        model = pickle.load(f)
    logger.info(f"Model loaded successfully. Expected features: {model.feature_names_in_}")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None

# FastAPI app
app = FastAPI(title="Crop Prediction API", version="1.0.0")


# Human readable
@app.get('/')
def home():
    return {'message':'Crop Prediction API'}


# machine readable
@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }


# Input model with aliases
class Prediction(BaseModel):
    N: float = Field(..., ge=0, alias="Nitrogen", description="Nitrogen Amount in Soil")
    P: float = Field(..., ge=0, alias="Phosphorus", description="Phosphorus Amount in Soil")
    K: float = Field(..., ge=0, alias="Potassium", description="Potassium Amount in Soil")
    temperature: float = Field(..., ge=0, alias="Temperature", description="Temperature in Celsius")
    humidity: float = Field(..., ge=0, alias="Humidity", description="Humidity in Air")
    ph: float = Field(..., ge=0, alias="PH", description="Soil pH")
    rainfall: float = Field(..., ge=0, alias="Rainfall", description="Rainfall in mm")

    class Config:
        allow_population_by_field_name = True


@app.post("/predict")
def predict_crop(data: Prediction):
    """
    Predict crop type based on input features
    """
    if model is None:
        raise HTTPException(status_code=500, detail='Model not loaded')

    try:
        # Use internal (trained) field names, not aliases
        input_data = data.dict(by_alias=False)
        input_df = pd.DataFrame([input_data])

        logger.info(f"Prediction input:\n{input_df}")

        prediction = model.predict(input_df)[0]
        return JSONResponse(status_code=200, content={"predicted_category": prediction})

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
