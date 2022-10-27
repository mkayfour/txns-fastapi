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

app = FastAPI(title="Transactions App")


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(tags.router)
app.include_router(transaction_tags.router)

models.Base.metadata.create_all(engine)
