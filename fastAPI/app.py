from contextlib import asynccontextmanager
from beanie import init_beanie
from predictive_models import load_model

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import BaseConfig
from motor import motor_asyncio
from mongo import User
import anyio

from .routers import user as user_router
from .routers import prediction as predict_router


settings = BaseConfig()
print(settings.DB_URL, settings.DB_NAME)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.client = motor_asyncio.AsyncIOMotorClient(settings.DB_URL)
    app.db = app.client[settings.DB_NAME]
    
    try:
        await app.client.admin.command("ping")
        print("Pinged your deployment. You have successfully connected to MongoDB!")
        print("Mongo address:", settings.DB_URL)
        await init_beanie(database=app.db, document_models=[User])
        print("Beanie models initialized")
    except Exception as e:
        print(e)

    try:
        # Offload the blocking sync MLflow call to a separate worker thread
        model, version, git_sha = await anyio.to_thread.run_sync(load_model)
        app.state.model = model
        app.state.model_version = version
        app.state.git_sha = git_sha
    except Exception as e:
        print(f"Critical Error: Could not load the MLflow model during startup: {e}")
        # Depending on your deployment preference, you can choose to let the app crash
        # or assign None so the app still runs other routes (e.g., /users)
        app.state.model = None
        app.state.model_version ="Unavailable"
    yield
    app.client.close()

app = FastAPI(lifespan=lifespan, root_path="/fastapi")
# app = FastAPI(lifespan=lifespan)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(predict_router.router, prefix="/predict", tags=["predict"])


@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "welcome to FastAPI app!"}