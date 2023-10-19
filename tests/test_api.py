import requests
from ..config import url_prediction,url_welcome


def test_root_endpoint_welcome_message():
    # Send a GET request to the root endpoint
    response = requests.get(url_welcome)

    # Assert that the response contains the expected welcome message
    assert response.status_code == 200
    assert response.json() == {"message": "Hello use /predict for the model prediction"}

#def test_model_loading():
#    
#    # Attempt to load the model
#    try:
#        pickle_file_path = "../volume_data/bike_pipeline_daily_predict.pkl" #get absolute path
#        loaded_pipeline = joblib.load(pickle_file_path)
#    except Exception as e:
#        loaded_pipeline = None
#
#    # Assert that the model is successfully loaded
#    assert loaded_pipeline is not None

def test_predict_endpoint_valid_request():
    # Define a valid input for the /predict endpoint
    input_data = {
        'instant': 1000,
        'dteday': '2024-02-01',
        'season': 3,
        'yr': 1,
        'mnth': 10,
        'holiday': 0,
        'weekday': 3,
        'workingday': 3,
        'weathersit': 3,
        'temp': 0.53,
        'atemp': 0.44,
        'hum': 0.21,
        'windspeed': 0.1,
        'casual': 300,
        'registered': 700,
        'cnt': 1000
    }

    # Send a POST request to the /predict endpoint with valid input data
    response = requests.post(url_prediction, json=input_data)
    # Assert that the response status code is 200
    assert response.status_code == 200


