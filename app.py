from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import pymysql

app = FastAPI()

# Load model
model = joblib.load("model.pkl")
preprocessor = joblib.load("preprocessor.pkl")


class CarInput(BaseModel):
    name: str
    year: int
    km_driven: int
    fuel: str
    seller_type: str
    transmission: str
    owner: str


@app.get("/")
def home():
    return {"message": "Car Price Prediction API Running"}


@app.post("/predict")
def predict(car: CarInput):

    df = pd.DataFrame([car.dict()])

    processed = preprocessor.transform(df)

    prediction = model.predict(processed)[0]

    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="Sivamani@123",
        database="world"
    )

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO prediction_logs
    (name,year,km_driven,fuel,
    seller_type,transmission,
    owner,predicted_price)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    """,
    (
        car.name,
        car.year,
        car.km_driven,
        car.fuel,
        car.seller_type,
        car.transmission,
        car.owner,
        float(prediction)
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "predicted_price": round(float(prediction), 2)
    }