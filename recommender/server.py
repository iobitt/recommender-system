from fastapi import FastAPI
from lib.services.prediction_service import PredictionService

app = FastAPI()

@app.get("/recommendations/{account_id}")
def recommendations(account_id: int, client_id: int):
    return {"product_ids": PredictionService.call(account_id, client_id)}
