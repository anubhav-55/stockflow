from fastapi import FastAPI

app = FastAPI(title="StockFlow API")

@app.get("/health")
def health_check():
	return {"status":"ok"}
