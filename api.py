from flask import Flask, request, render_template, flash, jsonify
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load('diabetes_prediction_model.pkl')

@app.route('/')
def home():
    return "the api is working"

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get data from the form
            gender = request.form['gender']
            age = request.form['age']
            hypertension = request.form['hypertension']
            heart_disease = request.form['heart_disease']
            smoking_history = request.form['smoking_history']
            bmi = request.form['bmi']
            HbA1c_level = request.form['HbA1c_level']
            blood_glucose_level = request.form['blood_glucose_level']

            # Validate input
            if not all([gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level]):
                flash('Please fill in all fields.')
                return jsonify({'error': 'Please fill in all fields.'}), 400

            # Convert to appropriate types
            age = float(age)
            hypertension = int(hypertension)
            heart_disease = int(heart_disease)
            bmi = float(bmi)
            HbA1c_level = float(HbA1c_level)
            blood_glucose_level = float(blood_glucose_level)

            # Prepare the data for prediction as a DataFrame
            input_data = pd.DataFrame({
                'gender': [gender],
                'age': [age],
                'hypertension': [hypertension],
                'heart_disease': [heart_disease],
                'smoking_history': [smoking_history],
                'bmi': [bmi],
                'HbA1c_level': [HbA1c_level],
                'blood_glucose_level': [blood_glucose_level]
            })

            # Make the prediction
            prediction = model.predict(input_data)

            # Return the result as JSON
            result = 'Diabetic' if prediction[0] == 1 else 'Non-diabetic'
            return jsonify({'prediction': result})
        
        except ValueError as e:
            return jsonify({'error': f"Invalid input: {str(e)}"}), 400

@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json()
    try:
        # Extract and validate input data
        required_fields = ['gender', 'age', 'hypertension', 'heart_disease', 'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Please provide all required fields.'}), 400

        # Convert to appropriate types
        age = float(data['age'])
        hypertension = int(data['hypertension'])
        heart_disease = int(data['heart_disease'])
        bmi = float(data['bmi'])
        HbA1c_level = float(data['HbA1c_level'])
        blood_glucose_level = float(data['blood_glucose_level'])
        gender = data['gender']

        # Prepare the data for prediction as a DataFrame
        input_data = pd.DataFrame({
            'gender': [gender],
            'age': [age],
            'hypertension': [hypertension],
            'heart_disease': [heart_disease],
            'smoking_history': [data['smoking_history']],
            'bmi': [bmi],
            'HbA1c_level': [HbA1c_level],
            'blood_glucose_level': [blood_glucose_level]
        })

        # Make the prediction
        prediction = model.predict(input_data)

        # Return the result as JSON
        result = 'Diabetic' if prediction[0] == 1 else 'Non-diabetic'
        return jsonify({'prediction': result})

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False) 