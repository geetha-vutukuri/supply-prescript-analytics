#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np

np.random.seed(42)
n_samples = 1000

data = {
    'shipment_id': range(1, n_samples + 1),
    'supplier_rating': np.random.uniform(3.0, 5.0, n_samples),
    'distance_miles': np.random.randint(500, 5000, n_samples),
    'weather_risk_index': np.random.uniform(0, 1, n_samples),
    'historical_lead_time': np.random.randint(5, 30, n_samples),
}

df = pd.DataFrame(data)
# Create a logical target variable: delays increase with lower supplier ratings and high weather risk
df['actual_delay_days'] = (
    (5 / df['supplier_rating']) 
    + (df['distance_miles'] / 1000) 
    + (df['weather_risk_index'] * 7) 
    + np.random.normal(0, 2, n_samples)
).round().astype(int)

# Ensure no negative delays
df['actual_delay_days'] = df['actual_delay_days'].clip(lower=0)
df.to_csv('Downloads/historical_shipments.csv', index=False)
print("Mock data generated successfully!")


# In[3]:


from sklearn.model_selection import train_test_split

# Features (X) and Target (y)
X = df[['supplier_rating', 'distance_miles', 'weather_risk_index', 'historical_lead_time']]
y = df['actual_delay_days']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# In[4]:





# In[5]:


from xgboost import XGBRegressor

# Create model
model = XGBRegressor()

# Train model
model.fit(X_train, y_train)


# In[6]:


y_pred = model.predict(X_test)


# In[7]:


from sklearn.metrics import mean_absolute_error, r2_score

print("MAE:", mean_absolute_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))


# In[8]:


import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# Load data
df = pd.read_csv('C:/Users/GEETHA/Downloads/historical_shipments.csv')
X = df[['supplier_rating', 'distance_miles', 'weather_risk_index', 'historical_lead_time']]
y = df['actual_delay_days']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=5)
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
import numpy as np

rmse = np.sqrt(mean_squared_error(y_test, predictions))
print(f"Model Baseline Trained. Root Mean Squared Error: {rmse:.2f} days")

# Save model artifact
import os

os.makedirs('ml_engine', exist_ok=True)
joblib.dump(model, 'ml_engine/xgboost_delay_model.pkl')


# In[9]:





# In[10]:


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="SupplyPrescript Engine")

# Load the trained model artifact
model = joblib.load('ml_engine/xgboost_delay_model.pkl')

class ShipmentFeatures(BaseModel):
    supplier_rating: float
    distance_miles: int
    weather_risk_index: float
    historical_lead_time: int

@app.get("/")
def home():
    return {"message": "Backend is working 🚀"}


@app.get("/")
def root():
    return {"status": "SupplyPrescript API running"}

@app.post("/predict-delay/")
def predict_delay(features: ShipmentFeatures):
    try:
        input_data = np.array([[
            features.supplier_rating,
            features.distance_miles,
            features.weather_risk_index,
            features.historical_lead_time
        ]])
        predicted_delay = model.predict(input_data)[0]
        return {"predicted_delay_days": max(0, float(round(predicted_delay, 1)))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

latest_decision = {
    "strategy": None,
    "predicted_delay": None,
    "actual_delay": None
}


class DecisionRequest(BaseModel):
    strategy: str
    predictedDelay: float


class FeedbackRequest(BaseModel):
    actualDelay: float


@app.post("/execute-decision")
def execute_decision(request: DecisionRequest):
    latest_decision["strategy"] = request.strategy
    latest_decision["predicted_delay"] = request.predictedDelay

    return {
        "success": True,
        "message": "Decision executed successfully.",
        "strategy": request.strategy,
        "predictedDelay": request.predictedDelay
    }


@app.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    latest_decision["actual_delay"] = request.actualDelay

    predicted = latest_decision["predicted_delay"]

    if predicted is None:
        error = None
    else:
        error = abs(predicted - request.actualDelay)

    return {
        "success": True,
        "message": "Feedback submitted successfully.",
        "actualDelay": request.actualDelay,
        "predictionError": error
    }


@app.get("/roi")
def roi():
    strategy = latest_decision["strategy"]
    predicted = latest_decision["predicted_delay"]
    actual = latest_decision["actual_delay"]

    if strategy is None:
        return {
            "roi": 0,
            "decision": "No decision yet",
            "cost": 0,
            "delay_reduction": 0
        }

    if strategy == "Air Freight":
        cost = 1200
        delay_reduction = 5
    elif strategy == "Buy from Supplier":
        cost = 700
        delay_reduction = 3
    else:
        cost = 300
        delay_reduction = 0

    if predicted is not None and actual is not None:
        improvement = max(0, predicted - actual)
        roi_value = round((improvement * 100) / max(cost / 100, 1), 2)
    else:
        roi_value = 0

    return {
        "roi": roi_value,
        "decision": strategy,
        "cost": cost,
        "delay_reduction": delay_reduction
    }
@app.post("/retrain")
def retrain_model():
    try:
        import pandas as pd
        import xgboost as xgb
        import joblib
        import os
        import numpy as np
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import mean_squared_error

        # Load the historical shipment data
        df = pd.read_csv(
            r"C:\Users\GEETHA\Downloads\historical_shipments.csv"
        )

        # Use the same 4 features as the prediction model
        X = df[
            [
                "supplier_rating",
                "distance_miles",
                "weather_risk_index",
                "historical_lead_time"
            ]
        ]

        y = df["actual_delay_days"]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        # Train new XGBoost model
        new_model = xgb.XGBRegressor(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=5
        )

        new_model.fit(X_train, y_train)

        # Evaluate new model
        predictions = new_model.predict(X_test)

        rmse = np.sqrt(
            mean_squared_error(y_test, predictions)
        )

        # Save the new model
        os.makedirs(
            r"C:\Users\GEETHA\ml_engine",
            exist_ok=True
        )

        joblib.dump(
            new_model,
            r"C:\Users\GEETHA\ml_engine\xgboost_delay_model.pkl"
        )

        # Update the model used by prediction endpoint
        global model
        model = new_model

        return {
            "message": "Model retrained successfully!",
            "rmse": round(float(rmse), 2),
            "features_used": 4
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# In[11]:


import matplotlib.pyplot as plt

plt.scatter(y_test, y_pred)
plt.xlabel("Actual Delay")
plt.ylabel("Predicted Delay")
plt.title("Actual vs Predicted")
plt.savefig("plot.png")


# In[12]:


df = pd.read_csv('C:/Users/GEETHA/Downloads/historical_shipments.csv')

X = df[['supplier_rating',
        'distance_miles',
        'weather_risk_index',
        'historical_lead_time']]

y = df['actual_delay_days']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = xgb.XGBRegressor(
    n_estimators=100,
    learning_rate=0.05,
    max_depth=5
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, predictions))

print(f"Model Baseline Trained. Root Mean Squared Error: {rmse:.2f} days")

os.makedirs('ml_engine', exist_ok=True)

joblib.dump(
    model,
    'ml_engine/xgboost_delay_model.pkl'
)

print("✅ 4-feature model saved successfully!")


# In[14]:


print(model)


# In[ ]:




