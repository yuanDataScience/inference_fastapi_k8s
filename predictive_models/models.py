from pydantic import BaseModel, Field


class InputFeatures(BaseModel):
    workclass: str = Field(...), 
    marital_status: str = Field(...),
    occupation: str = Field(...),
    relationship: str = Field(...),
    native_country: str = Field(...),
    race: str = Field(...),
    sex: str = Field(...),
    age: float = Field(...),
    fnlwgt: float = Field(...),
    education_num: float = Field(...),
    capital_gain: float = Field(...),
    capital_loss: float = Field(...),
    hours_per_week: float = Field(...)


class PredictOutput(BaseModel):
    prediction: bool = Field(...)


def load_model():
    pass




