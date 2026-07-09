from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rag.retriever import load_knowledge_base
from routes import analyze, facebook, infrastructure, mock, shield

app = FastAPI(title="IslamGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mock.router, prefix="/api")
app.include_router(analyze.router, prefix="/api")
app.include_router(shield.router, prefix="/api")
app.include_router(facebook.router, prefix="/api")
app.include_router(infrastructure.router, prefix="/api")


@app.on_event("startup")
def startup():
    load_knowledge_base()
