from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api import ping, notes
from app.db import engine, database, metadata

metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
