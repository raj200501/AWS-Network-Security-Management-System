import json
import boto3
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from botocore.exceptions import ClientError

# Initialize AWS clients
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

# Model and scaler file locations
model_bucket = 'network-security-models'
model_file = 'anomaly_model.pkl'
scaler_file = 'scaler.pkl'

# SNS topic for alerts
sns_topic_arn = 'arn:aws:sns:region:account-id:network-security-alerts'

# Load the model and scaler
def load_model_from_s3(bucket, key):
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return pickle.loads(response['Body'].read())

try:
    model = load_model_from_s3(model_bucket, model_file)
    scaler = load_model_from_s3(model_bucket, scaler_file)
except ClientError as e:
    print(f"Error loading model or scaler: {e}")

def detect_anomalies(data):
    data = scaler.transform([data])
    prediction = model.predict(data)
    return prediction[0] == -1

def lambda_handler(event, context):
    for record in event['Records']:
        payload = json.loads(record['body'])
        data = payload['data']
        
        if detect_anomalies(data):
            alert_message = f"Anomaly detected: {data}"
            sns_client.publish(TopicArn=sns_topic_arn, Message=alert_message)
            print(alert_message)

    return {'statusCode': 200, 'body': json.dumps('Processed')}
