from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import app.model as model_logic

# 1. Define the input schema
# Using Field to add basic validation (e.g., weights can't be negative)
class ChildData(BaseModel):
    Age_Months: int = Field(..., gt=0, lt=216) # Up to 18 years
    Weight_kg: float = Field(..., gt=0)
    Height_cm: float = Field(..., gt=0)
    Gender: str
    Region: str

app = FastAPI(title="Child Growth Classifier")

@app.get("/")
def root():
    """Health check endpoint to verify the server is running."""
    return {
        "status": "online",
        "engine": "algorithmic-math",
        "message": "Send a POST request to /predict"
    }

@app.post("/predict")
def predict(data: ChildData):
    """
    Receives child data and returns a classification:
    Wasted, Stunted, or Normal.
    """
    try:
        # Convert Pydantic object to a standard Python Dictionary
        input_dict = data.model_dump()
        
        # Call the logic from model.py
        prediction = model_logic.predict_single_child(input_dict)
        
        return {
            "prediction": prediction,
            "input_received": input_dict
        }
    except Exception as e:
        # If something goes wrong in the math logic, return a 500
        raise HTTPException(status_code=500, detail=str(e))