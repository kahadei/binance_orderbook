import models
from fastapi import FastAPI
from db import engine, SessionLocal
from routers import orders
from starlette.staticfiles import StaticFiles
from starlette import status
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders.router)
