from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os

app = Flask(__name__)
CORS(app)

# Load the model
try:
    model = joblib.load('diabetes_prediction_model.pkl')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {str(e)}")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "success",
        "message": "Diabetes Prediction API is running",
        "model_loaded": model is not None,
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
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No input data provided'
            }), 400

        required_fields = ['gender', 'age', 'hypertension', 'heart_disease', 
                         'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level']
        
        # Check if all required fields are present
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
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
        result = 'Diabetic' if prediction[0] == 1 else 'Non-diabetic'
        
        return jsonify({
            'status': 'success',
            'prediction': result,
            'input_received': data
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'input_received': request.get_json() if request.is_json else None
        }), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)