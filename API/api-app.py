import pandas as pd
import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, constr, conint
import joblib
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle

# Define the names of input features
input_features = ['model_key', 'mileage', 'engine_power', 'fuel', 'paint_color',
                  'car_type', 'private_parking_available', 'has_gps',
                  'has_air_conditioning', 'automatic_car', 'has_getaround_connect',
                  'has_speed_regulator', 'winter_tires']

# Define numeric and categorical features based on input_features
numeric_features = ['mileage', 'engine_power']
categorical_features = [feature for feature in input_features if feature not in numeric_features]

class RentalPredictionFeatures(BaseModel):
    model_key: constr(min_length=1, regex='^(Citroën|Peugeot|PGO|Renault|Audi|BMW|Ford|Mercedes|Opel|Porsche|Volkswagen|KIA Motors|Alfa Romeo|Ferrari|Fiat|Lamborghini|Maserati|Lexus|Honda|Mazda|Mini|Mitsubishi|Nissan|SEAT|Subaru|Suzuki|Toyota|Yamaha)$')
    mileage: conint(ge=0, le=300000)
    engine_power: conint(ge=0, le=300)
    fuel: constr(regex='^(diesel|petrol|hybrid_petrol|electro)$')
    paint_color: constr(regex='^(black|grey|white|red|silver|blue|orange|beige|brown|green)$')
    car_type: constr(regex='^(convertible|coupe|estate|hatchback|sedan|subcompact|suv|van)$')
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool

description = """
Welcome to this Getaround API ! Dear car owner, here you can get a suggested optimum price for rental.
Just give us some information about your car, and we will suggest you the best price for you to rent your vehicle.
Let's try it out !
"""

tag_metadata = [
    {
        "name": "Introduction Endpoint",
        "description": "Redirect to documentation"
    },
    {
        "name": "Predictions",
        "description": "Post some data and get predictions in exchange !"
    },
]

app = FastAPI(
    title="Getaround rental pricing optimization",
    description=description,
    version="0.1",
    contact={
        "name": "Caroline Mathius",
        "url": "https://github.com/carolinemathius",
    },
    openapi_tags=tag_metadata
)

# Load trained model
model = joblib.load("best_model.pkl")

# Load the preprocessor
with open('preprocessor.pkl', 'rb') as file:
    preprocessor = pickle.load(file)

# Define the FastAPI endpoints
@app.get("/", tags=["Introduction Endpoint"])
async def docs_redirect():
    """Simply redirects to /docs"""
    return RedirectResponse(url='/docs')

@app.post("/predictions", tags=["Predictions"])
async def predict(prfeatures: RentalPredictionFeatures):
    try:
        # Convert input data to a dictionary for prediction
        input_data = {
            "model_key": [prfeatures.model_key],
            "mileage": [prfeatures.mileage],
            "engine_power": [prfeatures.engine_power],
            "fuel": [prfeatures.fuel],
            "paint_color": [prfeatures.paint_color],
            "car_type": [prfeatures.car_type],
            "private_parking_available": [prfeatures.private_parking_available],
            "has_gps": [prfeatures.has_gps],
            "has_air_conditioning": [prfeatures.has_air_conditioning],
            "automatic_car": [prfeatures.automatic_car],
            "has_getaround_connect": [prfeatures.has_getaround_connect],
            "has_speed_regulator": [prfeatures.has_speed_regulator],
            "winter_tires": [prfeatures.winter_tires],
        }

        # Create a DataFrame from the input data with the defined feature names
        input_df = pd.DataFrame(input_data, columns=input_features)
        print("Performing preprocessings...")
        print(input_df.head())
        print()

        # Preprocess the input data using the loaded preprocessor
        preprocessed_data = preprocessor.transform(input_df)
        print('...Done.')
        print(preprocessed_data[0:5])
        
        # Perform the prediction
        prediction = model.predict(preprocessed_data)

        # Return the prediction or any other response
        return {"prediction": prediction.tolist()}  # Convert prediction to a list

    except Exception as e:
        # Capture and log the exception details
        print(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)
