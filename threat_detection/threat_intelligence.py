import boto3
import json

# Initialize AWS clients
dynamodb_client = boto3.client('dynamodb')
sns_client = boto3.client('sns')

# DynamoDB table for threat intelligence
threat_intel_table = 'ThreatIntelligence'

# SNS topic for alerts
sns_topic_arn = 'arn:aws:sns:region:account-id:network-security-alerts'

def check_threat_intelligence(ip_address):
    response = dynamodb_client.get_item(
        TableName=threat_intel_table,
        Key={'IPAddress': {'S': ip_address}}
    )
    if 'Item' in response:
        return True
    return False

def lambda_handler(event, context):
    for record in event['Records']:
        payload = json.loads(record['body'])
        ip_address = payload['ip_address']
        
        if check_threat_intelligence(ip_address):
            alert_message = f"Threat detected from IP: {ip_address}"
            sns_client.publish(TopicArn=sns_topic_arn, Message=alert_message)
            print(alert_message)

    return {'statusCode': 200, 'body': json.dumps('Processed')}
