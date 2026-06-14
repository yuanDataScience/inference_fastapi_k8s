from fastapi import APIRouter, Body, status
from ..authentication import AuthHandler
from predictive_models import (InputFeatures, PredictOutput, load_model)


auth_handler = AuthHandler()
router = APIRouter()


@router.post("/", response_model=PredictOutput, status_code=status.HTTP_200_OK)
async def predict(input_features: InputFeatures = Body(...)):
    model = load_model()

    predict_rs = model.predict(input_features)

    return False if predict_rs == 0 else True
