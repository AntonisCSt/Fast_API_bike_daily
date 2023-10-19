import requests
import pandas as pd
from config import url_prediction #url for Fast_API prediction endpoint

# Load the input data from day_inference.csv
input_data = pd.read_csv("day_inference.csv")

# Convert the input data to a list of dictionaries
input_data_list = input_data.to_dict(orient="records")

# Make POST requests for each input data instance
predictions = []

for instance in input_data_list:
    response = requests.post(url_prediction, json=instance)
    if response.status_code == 200:
        result = response.json()
        predictions.append(result["predictions"])
    else:
        print(f"Prediction failed for instance: {instance}")

# predictions now contains the model's predictions for each input data instance
print(predictions)
