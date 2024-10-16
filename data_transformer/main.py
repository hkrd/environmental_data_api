from fastapi import FastAPI
from data_transformer.routes import router

app = FastAPI()

app.include_router(router)
