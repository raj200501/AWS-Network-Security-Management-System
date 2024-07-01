import boto3
import json

# Initialize AWS clients
s3_client = boto3.client('s3')
cloudwatch_client = boto3.client('logs')

# S3 bucket for aggregated logs
aggregated_logs_bucket = 'network-security-aggregated-logs'

def aggregate_logs(log_group_name, log_stream_name, start_time, end_time):
    response = cloudwatch_client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        startTime=start_time,
        endTime=end_time,
        limit=100,
        startFromHead=True
    )
    return response['events']

def lambda_handler(event, context):
    log_group_name = event['log_group_name']
    log_stream_name = event['log_stream_name']
    start_time = event['start_time']
    end_time = event['end_time']
    
    logs = aggregate_logs(log_group_name, log_stream_name, start_time, end_time)
    
    aggregated_log_key = f"aggregated_logs_{log_stream_name}_{start_time}_{end_time}.json"
    s3_client.put_object(
        Bucket=aggregated_logs_bucket,
        Key=aggregated_log_key,
        Body=json.dumps(logs)
    )
    return {'statusCode': 200, 'body': json.dumps('Log aggregation completed')}
