
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from model.predict import predict_output,model,MODEL_VERSION
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse


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

@app.post("/predict",response_model=PredictionResponse)
def predict_crop(data: UserInput):
    """
    Predict crop type based on input features
    """

    user_input={
        'N':data.N,
        
        'P':data.P,
        
        'K': data.K,  
        'temperature': data.temperature,
        'humidity':data.humidity,
        
        'ph':data.ph,
        
        'rainfall':data.rainfall,
        
    }
    
    try:
        # Use internal (trained) field names, not aliases
        # input_data = data.dict(by_alias=False)
        # input_df = pd.DataFrame([input_data])
        


        prediction = predict_output(user_input)
        return JSONResponse(status_code=200, content={"predicted_category": prediction})

    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
