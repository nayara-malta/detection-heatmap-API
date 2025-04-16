from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.heatmap import router as heatmap_router

app = FastAPI(title="Detection Heatmap API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.include_router(heatmap_router, prefix="/api", tags=["Heatmap"])

@app.get("/")
def read_root():
    """
    Endpoint raiz da API.

    Retorna:
        dict: Um dicionário contendo uma mensagem de boas-vindas.
    """
    return {"message": "Welcome to the Detection Heatmap API!"}