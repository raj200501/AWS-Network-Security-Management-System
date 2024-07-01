import boto3
import pickle

# Initialize AWS clients
s3_client = boto3.client('s3')

# S3 bucket for models
model_bucket = 'network-security-models'

def save_model_to_s3(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name
    with open(file_name, "rb") as f:
        s3_client.upload_fileobj(f, bucket, object_name)

if __name__ == '__main__':
    save_model_to_s3('models/anomaly_model.pkl', model_bucket)
    save_model_to_s3('models/scaler.pkl', model_bucket)
    print("Model saved to S3")
