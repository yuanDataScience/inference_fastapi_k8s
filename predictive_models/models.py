from pydantic import BaseModel, Field, ConfigDict
import os
import mlflow
from mlflow.sklearn import Model
from fastAPI.config import BaseConfig
from mlflow.tracking import MlflowClient


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
    prediction: list[bool] = Field(...)
    version: str = Field(...)
    git_sha: str = Field(...)


def load_model() -> tuple[Model, str, str]:
    try:
        model_name = "adult_model"
        model_uri = f"models:/{model_name}/latest"

        # 1. Initialize the MlflowClient to query metadata
        client = MlflowClient()

        # 1. Search for all registered versions of this model name
        # This bypasses stages entirely and works seamlessly with modern MLflow versions
        model_versions = client.search_model_versions(f"name='{model_name}'")

        git_sha = "unknown"
        model_version = "unknown"

        if model_versions:
            latest_version_obj = model_versions[0]
            model_version = latest_version_obj.version

            # 2. Extract the 'git_sha' tag you set using client.set_model_version_tag
            # It lives inside the .tags dictionary of the model version object
            git_sha = latest_version_obj.tags.get("git_sha", "unknown")
        else:
            model_version = "unknown"
            git_sha = "unknown"

        print(f"Loading model from {model_uri}...")
        model = mlflow.sklearn.load_model(model_uri)
        print("Model loaded successfully!")

        return model, model_version, git_sha
    except Exception as e:
        print(f"Failed to load model from MLflow: {e}")
        raise e




