from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load('diabetes_prediction_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Extract data from JSON
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
            'prediction': result
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)