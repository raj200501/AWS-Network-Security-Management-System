import boto3
import json
from datetime import datetime
from kinesis_consumer import KinesisConsumer

# Initialize AWS clients
kinesis_client = boto3.client('kinesis')
lambda_client = boto3.client('lambda')

# Kinesis stream details
stream_name = 'network-security-stream'

# Lambda function details
anomaly_detection_lambda = 'arn:aws:lambda:region:account-id:function:anomaly-detection-function'

def process_records(records):
    for record in records:
        payload = json.loads(record['Data'])
        # Process the record (e.g., send to Lambda for anomaly detection)
        response = lambda_client.invoke(
            FunctionName=anomaly_detection_lambda,
            InvocationType='Event',
            Payload=json.dumps(payload)
        )
        print(f"Invoked anomaly detection Lambda: {response}")

def main():
    consumer = KinesisConsumer(stream_name, process_records)
    consumer.run()

if __name__ == '__main__':
    main()
