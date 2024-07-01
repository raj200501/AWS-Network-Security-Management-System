import pandas as pd
import pickle
from sklearn.metrics import classification_report

def evaluate_anomaly_model():
    data = pd.read_csv('data/processed_data.csv')
    features = data[['feature1', 'feature2', 'feature3']]  # Example features
    true_labels = data['label']
    
    with open('models/anomaly_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    
    with open('models/scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    
    scaled_features = scaler.transform(features)
    predictions = model.predict(scaled_features)
    predictions = [1 if p == -1 else 0 for p in predictions]  # Convert -1 to 1 (anomaly) and 1 to 0 (normal)
    
    report = classification_report(true_labels, predictions)
    print(report)

if __name__ == '__main__':
    evaluate_anomaly_model()
    print("Model evaluation complete")
