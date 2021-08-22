import uvicorn
from fastapi import FastAPI
import numpy as np
from artifacts import lmodel_weights
from pydantic import BaseModel

app = FastAPI()


class RideInfo(BaseModel):
    id: str
    pickup_datetime: str
    pickup_longitude: float
    pickup_latitude: float
    dropoff_longitude: float
    dropoff_latitude: float
    passenger_count: int


@app.post("/predict")
async def predict(ride_info: RideInfo):
    payload = ride_info.dict()
    abs_diff_longitude = abs(
        payload.get("pickup_longitude", 0) - payload.get("dropoff_longitude", 0)
    )
    abs_diff_latitude = abs(
        payload.get("pickup_latitude", 0) - payload.get("dropoff_latitude", 0)
    )
    data = np.array([abs_diff_longitude, abs_diff_latitude, 1])
    prediction = np.matmul(data, lmodel_weights).round(decimals=2)
    return {"price": prediction}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
