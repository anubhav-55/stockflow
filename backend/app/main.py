from fastapi import FastAPI

from app.api.routes.categories import router as categories_router



app = FastAPI(title="StockFlow API")

app.include_router(categories_router)

@app.get("/health")
def health_check():
	return {"status":"ok"}
