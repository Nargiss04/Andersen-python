from fastapi import FastAPI
from app.routes import users, tasks
from app.database import database

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(users.router)
app.include_router(tasks.router)
