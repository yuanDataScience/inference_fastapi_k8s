from pydantic import BaseModel, Field, ConfigDict
import os
import mlflow
from mlflow.sklearn import Model
from fastAPI.config import BaseConfig


settings = BaseConfig()

# 1. Configure the connection to your MLflow and S3/MinIO backend
os.environ["AWS_DEFAULT_REGION"] = settings.AWS_DEFAULT_REGION
os.environ["MLFLOW_S3_ENDPOINT_URL"] = settings.MLFLOW_S3_ENDPOINT_URL
os.environ["MLFLOW_BOTO_CLIENT_ADDRESSING_STYLE"] = settings.MLFLOW_BOTO_CLIENT_ADDRESSING_STYLE
os.environ["AWS_ACCESS_KEY_ID"] = settings.AWS_ACCESS_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"] = settings.AWS_SECRET_ACCESS_KEY
mlflow.set_tracking_uri(settings.mlflow_tracking_uri)


class InputFeatures(BaseModel):
    workclass: str = Field(...)
    marital_status: str = Field(..., alias="marital-status")
    occupation: str = Field(...)
    relationship: str = Field(...)
    native_country: str = Field(..., alias="native-country")
    race: str = Field(...)
    sex: str = Field(...)
    age: float = Field(...)
    fnlwgt: float = Field(...)
    education_num: float = Field(..., alias="education-num")
    capital_gain: float = Field(..., alias="capital-gain")
    capital_loss: float = Field(..., alias="capital-loss")
    hours_per_week: float = Field(..., alias="hours-per-week")

    model_config = ConfigDict(populate_by_name=True)


class PredictOutput(BaseModel):
    prediction: bool = Field(...)


def load_model() -> Model:
    try:
        model_name = "adult_model"
        model_uri = f"models:/{model_name}/latest"

        print(f"Loading model from {model_uri}...")
        model = mlflow.sklearn.load_model(model_uri)
        print("Model loaded successfully!")

        return model
    except Exception as e:
        print(f"Failed to load model from MLflow: {e}")
        raise e




