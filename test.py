import requests

# Define the API endpoint
url = 'http://192.168.1.2:8000/api/predict'  # Adjust if your API is hosted elsewhere

# Sample data for testing
test_data = [
    {
        "gender": "Female",
        "age": 80.0,
        "hypertension": 0,
        "heart_disease": 1,
        "smoking_history": "never",
        "bmi": 27.32,
        "HbA1c_level": 6.6,
        "blood_glucose_level": 85,
        "actual": 0  # Non-diabetic
    },
    {
        "gender": "Male",
        "age": 54.0,
        "hypertension": 0,
        "heart_disease": 0,
        "smoking_history": "No Info",
        "bmi": 27.32,
        "HbA1c_level": 6.6,
        "blood_glucose_level": 80,
        "actual": 0  # Non-diabetic
    },
    {
        "gender": "Female",
        "age": 44.0,
        "hypertension": 0,
        "heart_disease": 0,
        "smoking_history": "never",
        "bmi": 19.31,
        "HbA1c_level": 6.5,
        "blood_glucose_level": 200,
        "actual": 1  # Diabetic
    }
]

# Test the API with the sample data
for i, data in enumerate(test_data):
    response = requests.post(url, json=data)
    prediction = response.json().get('prediction')
    actual = data['actual']
    print(f"Test Case {i + 1}:")
    print(f"Input: {data}")
    print(f"Predicted: {prediction}, Actual: {'Diabetic' if actual == 1 else 'Non-diabetic'}")
    print("-" * 50)