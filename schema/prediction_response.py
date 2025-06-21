from pydantic import BaseModel, Field
from typing import Dict


class PredictionResponse(BaseModel):
    predicted_category: str = Field(
        ...,
        description="The predicted crop category",
        example="jute"
    )
    confidence: float = Field(
        ...,
        ge=0, le=1,
        description="Confidence score (range: 0 to 1)",
        example=0.9772
    )
    class_probabilities: Dict[str, float] = Field(
        ...,
        description="Probabilities for each class",
        example={
            "apple": 0.0,
            "jute": 0.9772,
            "maize": 0.0209,
            "rice": 0.0014
        }
    )
