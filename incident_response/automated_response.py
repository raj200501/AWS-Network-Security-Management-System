import boto3
import json

# Initialize AWS clients
ec2_client = boto3.client('ec2')
sns_client = boto3.client('sns')

# SNS topic for alerts
sns_topic_arn = 'arn:aws:sns:region:account-id:network-security-alerts'

def quarantine_instance(instance_id):
    response = ec2_client.modify_instance_attribute(
        InstanceId=instance_id,
        Groups=[]
    )
    return response

def lambda_handler(event, context):
    for record in event['Records']:
        payload = json.loads(record['body'])
        instance_id = payload['instance_id']
        
        response = quarantine_instance(instance_id)
        sns_client.publish(TopicArn=sns_topic_arn, Message=f"Instance quarantined: {instance_id}")
        print(f"Instance quarantined: {instance_id}, Response: {response}")

    return {'statusCode': 200, 'body': json.dumps('Processed')}
