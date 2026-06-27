# Customer Churn Predictor — Render Deployment

## Project Structure
```
churn-app/
├── app.py                 # Flask API
├── model.sav              # Trained Random Forest model  ← YOU ADD THIS
├── feature_columns.pkl    # Feature column list          ← YOU ADD THIS
├── templates/
│   └── index.html         # Frontend UI
├── requirements.txt
├── Procfile
└── .gitignore
```

## Step-by-Step Deployment on Render

### 1. Export model files from Colab
Run this in your Colab notebook and download both files:
```python
from google.colab import files
files.download('model.sav')
files.download('feature_columns.pkl')
```

### 2. Set up GitHub repo
```bash
git init
git add .
git commit -m "Initial commit"
# Create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/churn-app.git
git push -u origin main
```

### 3. Deploy on Render
1. Go to https://render.com and sign up/log in
2. Click **New → Web Service**
3. Connect your GitHub repo
4. Fill in:
   - **Name:** customer-churn-predictor
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
5. Click **Create Web Service**
6. Wait ~3-5 minutes for the build to finish
7. Your app will be live at `https://your-app-name.onrender.com`

## Local Testing
```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

## API Usage
POST `/predict` with JSON body:
```json
{
  "gender": "Male",
  "SeniorCitizen": 0,
  "Partner": "No",
  "Dependents": "No",
  "tenure_group": "1 - 12",
  "PhoneService": "Yes",
  "MultipleLines": "No",
  "InternetService": "Fiber optic",
  "OnlineSecurity": "No",
  "OnlineBackup": "No",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "No",
  "StreamingMovies": "No",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 70.5,
  "TotalCharges": 150.0
}
```

Response:
```json
{
  "churn": 1,
  "churn_label": "Yes",
  "churn_probability": 82.4
}
```
