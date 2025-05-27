from fastapi import FastAPI
from routes import document
from logging_config import setup_logging
setup_logging()



app = FastAPI()

app.include_router(document.router)
