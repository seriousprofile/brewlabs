from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import Base, engine
from routers import brews


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="ColdBrews API", version="0.1.0", lifespan=lifespan)
app.include_router(brews.router)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}
