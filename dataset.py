# dataset.py
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Download the dataset from UCI
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"

# Column names
columns = ["age","sex","cp","trestbps","chol","fbs","restecg","thalach",
           "exang","oldpeak","slope","ca","thal","target"]

# Load dataset
df = pd.read_csv(url, names=columns)

# Replace '?' with NaN and drop missing rows
df.replace('?', pd.NA, inplace=True)
df.dropna(inplace=True)

# Convert all columns to numeric
df = df.apply(pd.to_numeric)

# Split features and target
X = df.drop("target", axis=1).values
y = df["target"].apply(lambda x: 1 if x > 0 else 0).values  # binary classification

# Standardize features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Function to split dataset among clients
def load_data(client_id=0, num_clients=2):
    # Split data among clients
    X_split = np.array_split(X, num_clients)
    y_split = np.array_split(y, num_clients)
    
    # Train-test split for this client
    X_train, X_test, y_train, y_test = train_test_split(
        X_split[client_id], y_split[client_id], test_size=0.2, random_state=42
    )
    
    return X_train, y_train, X_test, y_test
