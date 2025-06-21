import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field



class UserInput(BaseModel):
    N: float = Field(..., ge=0, alias="Nitrogen", description="Nitrogen Amount in Soil")
    P: float = Field(..., ge=0, alias="Phosphorus", description="Phosphorus Amount in Soil")
    K: float = Field(..., ge=0, alias="Potassium", description="Potassium Amount in Soil")
    temperature: float = Field(..., ge=0, alias="Temperature", description="Temperature in Celsius")
    humidity: float = Field(..., ge=0, alias="Humidity", description="Humidity in Air")
    ph: float = Field(..., ge=0, alias="PH", description="Soil pH")
    rainfall: float = Field(..., ge=0, alias="Rainfall", description="Rainfall in mm")

    class Config:
        allow_population_by_field_name = True

