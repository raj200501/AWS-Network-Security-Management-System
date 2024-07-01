import boto3
import json
from datetime import datetime

# Initialize AWS clients
sns_client = boto3.client('sns')
s3_client = boto3.client('s3')

# SNS topic for alerts
sns_topic_arn = 'arn:aws:sns:region:account-id:network-security-alerts'

# S3 bucket for incident logs
incident_logs_bucket = 'network-security-incident-logs'

def handle_incident(incident):
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    incident_log_key = f"incident_{timestamp}.json"
    s3_client.put_object(
        Bucket=incident_logs_bucket,
        Key=incident_log_key,
        Body=json.dumps(incident)
    )
    sns_client.publish(TopicArn=sns_topic_arn, Message=json.dumps(incident))
    print(f"Incident logged and alert sent: {incident}")

def lambda_handler(event, context):
    for record in event['Records']:
        payload = json.loads(record['body'])
        incident = payload['incident']
        handle_incident(incident)

    return {'statusCode': 200, 'body': json.dumps('Processed')}
