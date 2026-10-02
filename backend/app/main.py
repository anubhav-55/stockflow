from fastapi import FastAPI

from app.api.routes.categories import router as categories_router
from app.api.routes.products import router as products_router



app = FastAPI(title="StockFlow API")

app.include_router(categories_router)
app.include_router(products_router)

@app.get("/health")
def health_check():
	return {"status":"ok"}
