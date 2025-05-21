from fastapi import FastAPI, APIRouter
from app.routes import router
from fastapi.responses import HTMLResponse

app = FastAPI(title="API de Transcripción con Azure y YouTube")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "API funcionando"}

