from fastapi import FastAPI
from app.db.init_db import init_db

app = FastAPI(title="StockFlow API")

# @app.on_event("startup")
# def startup() -> None:
# 	init_db()

@app.get("/health")
def health_check():
	return {"status":"ok"}
