# Diabetes Prediction API

This project is a Flask-based API for predicting diabetes based on user input. It uses a pre-trained model to make predictions and provides endpoints for both web form submissions and JSON requests.

## Requirements

Before running the API, ensure you have the following dependencies installed. You can install them using pip:

```bash
pip install -r requirements.txt
```


## Running the API

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Start the Flask API**:
   Run the following command in your terminal:
   ```bash
   python api.py
   ```
   The API will start running on `http://0.0.0.0:8000`.

## Testing the API

You can test the API using the provided `test.py` script. This script sends sample data to the `/api/predict` endpoint and prints the predictions.

1. **Run the test script**:
   Open another terminal window and run:
   ```bash
   python test.py
   ```

2. **Expected Output**:
   The script will output the predictions for each test case, comparing them with the actual values.

## API Endpoints

### Home Endpoint

- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns a simple message indicating that the API is working.

### Prediction Endpoint

- **URL**: `/api/predict`
- **Method**: `POST`
- **Request Body**: JSON object containing the following fields:
  - `gender`: (string) Gender of the patient (e.g., "Male", "Female")
  - `age`: (float) Age of the patient
  - `hypertension`: (int) Hypertension status (0 or 1)
  - `heart_disease`: (int) Heart disease status (0 or 1)
  - `smoking_history`: (string) Smoking history (e.g., "never", "formerly", "currently")
  - `bmi`: (float) Body Mass Index
  - `HbA1c_level`: (float) HbA1c level
  - `blood_glucose_level`: (float) Blood glucose level

- **Response**: JSON object containing the prediction:
  - `prediction`: (string) "Diabetic" or "Non-diabetic"
