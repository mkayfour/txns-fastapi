"""
Main app
"""
from fastapi import FastAPI
from db import models
from db.database import engine

from router import transactions
from router import tags
from router import users
from router import transaction_tags

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Transactions App")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(tags.router)
app.include_router(transaction_tags.router)

models.Base.metadata.create_all(engine)
