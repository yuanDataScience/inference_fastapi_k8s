from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from pathlib import Path


class InputFeatures(BaseModel):
    workclass: str = Field(...), 
    marital-status: str = Field(...),
    occupation: str = Field(...),
    relationship: str = Field(...),
    native-country: str = Field(...),
    race: str = Field(...),
    sex: str = Field(...),
    age: float = Field(...),
    fnlwgt: float = Field(...),
    education-num: float = Field(...),
    capital-gain: float = Field(...),
    capital-loss: float = Field(...),
    hours-per-week: float = Field(...)   




