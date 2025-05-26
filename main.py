from fastapi import FastAPI
from routes import document



app = FastAPI()

app.include_router(document.router)
