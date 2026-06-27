from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load model and feature columns
model = pickle.load(open('model.sav', 'rb'))
feature_columns = pickle.load(open('feature_columns.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Build a raw input dict matching original df1 columns (before get_dummies)
        raw = {
            'SeniorCitizen': int(data.get('SeniorCitizen', 0)),
            'MonthlyCharges': float(data.get('MonthlyCharges', 0)),
            'TotalCharges': float(data.get('TotalCharges', 0)),
            'gender': data.get('gender', 'Male'),
            'Partner': data.get('Partner', 'No'),
            'Dependents': data.get('Dependents', 'No'),
            'PhoneService': data.get('PhoneService', 'No'),
            'MultipleLines': data.get('MultipleLines', 'No phone service'),
            'InternetService': data.get('InternetService', 'DSL'),
            'OnlineSecurity': data.get('OnlineSecurity', 'No'),
            'OnlineBackup': data.get('OnlineBackup', 'No'),
            'DeviceProtection': data.get('DeviceProtection', 'No'),
            'TechSupport': data.get('TechSupport', 'No'),
            'StreamingTV': data.get('StreamingTV', 'No'),
            'StreamingMovies': data.get('StreamingMovies', 'No'),
            'Contract': data.get('Contract', 'Month-to-month'),
            'PaperlessBilling': data.get('PaperlessBilling', 'No'),
            'PaymentMethod': data.get('PaymentMethod', 'Electronic check'),
            'tenure_group': data.get('tenure_group', '1 - 12'),
        }

        input_df = pd.DataFrame([raw])
        input_dummies = pd.get_dummies(input_df)

        # Align columns with training data
        input_aligned = input_dummies.reindex(columns=feature_columns, fill_value=0)

        prediction = model.predict(input_aligned)[0]
        probability = model.predict_proba(input_aligned)[0][1]

        return jsonify({
            'churn': int(prediction),
            'churn_label': 'Yes' if prediction == 1 else 'No',
            'churn_probability': round(float(probability) * 100, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False)
