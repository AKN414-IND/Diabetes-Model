from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Load the model
try:
    model = joblib.load('diabetes_prediction_model.pkl')
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    model = None

@app.route('/', methods=['GET'])
def home():
    model_status = model is not None
    logger.info(f"Home endpoint accessed. Model loaded: {model_status}")
    return jsonify({
        "status": "success",
        "message": "Diabetes Prediction API is running",
        "model_loaded": model_status,
        "model_version": "1.6.1",
        "how_to_use": {
            "endpoint": "/predict",
            "method": "POST",
            "input_format": {
                "gender": "string (Male/Female)",
                "age": "float",
                "hypertension": "int (0/1)",
                "heart_disease": "int (0/1)",
                "smoking_history": "string",
                "bmi": "float",
                "HbA1c_level": "float",
                "blood_glucose_level": "float"
            }
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        logger.error("Prediction attempted but model is not loaded")
        return jsonify({
            'status': 'error',
            'message': 'Model not loaded'
        }), 500

    try:
        data = request.get_json()
        logger.info(f"Received prediction request with data: {data}")
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No input data provided'
            }), 400

        # Create DataFrame
        input_data = pd.DataFrame({
            'gender': [data['gender']],
            'age': [float(data['age'])],
            'hypertension': [int(data['hypertension'])],
            'heart_disease': [int(data['heart_disease'])],
            'smoking_history': [data['smoking_history']],
            'bmi': [float(data['bmi'])],
            'HbA1c_level': [float(data['HbA1c_level'])],
            'blood_glucose_level': [float(data['blood_glucose_level'])]
        })
        
        # Make prediction
        prediction = model.predict(input_data)
        probability = model.predict_proba(input_data)[0]
        result = 'Diabetic' if prediction[0] == 1 else 'Non-diabetic'
        
        response = {
            'status': 'success',
            'prediction': result,
            'confidence': float(max(probability)),
            'input_received': data
        }
        logger.info(f"Prediction made successfully: {response}")
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'input_received': request.get_json() if request.is_json else None
        }), 400

if __name__ == '__main__':
    # Get port from environment variable or default to 10000
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)