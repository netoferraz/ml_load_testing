# LOAD TEST FOR NYC PRICE FARE

First of all, you need to download the training [dataset](https://www.kaggle.com/c/new-york-city-taxi-fare-prediction/data) from the New York City Taxi Fare Prediction and put it into `./data` folder.

## 1. serving the model

### 1.1 build
```
docker build --tag="nyc/lmodel-price-fare:v0.1" .
```

### 1.2 run
```
docker run -p 8000:8000 nyc/lmodel-price-fare:v0.1
```

## 2. locust
### start locust server

```
locust -f ./tests/locust/random.py
```

Once this was done you can access locust ui available at `localhost:8089`.