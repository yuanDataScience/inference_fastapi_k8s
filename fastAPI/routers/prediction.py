from fastapi import APIRouter, Body, status, Request, HTTPException
from ..authentication import AuthHandler
from predictive_models import (InputFeatures, PredictOutput)
import pandas as pd


auth_handler = AuthHandler()
router = APIRouter()


@router.post("/", response_model=PredictOutput, status_code=status.HTTP_200_OK)
def make_prediction(request: Request, data: InputFeatures = Body(...)):
    # Retrieve the single in-memory model pointer from app.state
    model = getattr(request.app.state, "model", None)

    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Machine learning model is not loaded or currently unavailable."
        )

    try:
        # Convert Pydantic object directly into a Pandas DataFrame
        # Force export specifically using the alias names
        # using warnings=False or by reconstructing via field aliases
        input_dict = {
            (InputFeatures.model_fields[k].alias or k): v
            for k, v in data.model_dump().items()
        }

        # Build the DataFrame from the guaranteed hyphenated dictionary
        input_df = pd.DataFrame([input_dict])

        # Execute the prediction directly on the main thread pool worker
        prediction = model.predict(input_df)[0]
        prediction_rs = False if prediction == 0 else True


        # Return the prediction result
        return {"prediction": prediction_rs}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Inference pipeline execution failed: {str(e)}"
        )
