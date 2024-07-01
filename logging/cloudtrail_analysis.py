import boto3
import json
from datetime import datetime, timedelta

# Initialize AWS clients
cloudtrail_client = boto3.client('cloudtrail')
s3_client = boto3.client('s3')

# S3 bucket for CloudTrail logs
cloudtrail_logs_bucket = 'network-security-cloudtrail-logs'

def get_cloudtrail_events(start_time, end_time):
    response = cloudtrail_client.lookup_events(
        StartTime=start_time,
        EndTime=end_time,
        MaxResults=50
    )
    return response['Events']

def analyze_events(events):
    # Example analysis: count the number of "TerminateInstances" events
    terminate_instances_events = [event for event in events if event['EventName'] == 'TerminateInstances']
    return len(terminate_instances_events)

def lambda_handler(event, context):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=15)
    
    events = get_cloudtrail_events(start_time, end_time)
    analysis_result = analyze_events(events)
    
    log_key = f"cloudtrail_analysis_{end_time.strftime('%Y%m%dT%H%M%SZ')}.json"
    s3_client.put_object(
        Bucket=cloudtrail_logs_bucket,
        Key=log_key,
        Body=json.dumps({'terminate_instances_events_count': analysis_result})
    )
    return {'statusCode': 200, 'body': json.dumps('CloudTrail analysis completed')}
