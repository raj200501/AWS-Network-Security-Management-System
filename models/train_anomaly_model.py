import pandas as pd
import pickle
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def train_anomaly_model():
    data = pd.read_csv('data/processed_data.csv')
    features = data[['feature1', 'feature2', 'feature3']]  # Example features
    
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    model = IsolationForest(contamination=0.01, random_state=42)
    model.fit(scaled_features)
    
    with open('models/anomaly_model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)
    
    with open('models/scaler.pkl', 'wb') as scaler_file:
        pickle.dump(scaler, scaler_file)
    
    print("Model training complete")

if __name__ == '__main__':
    train_anomaly_model()
