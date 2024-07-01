import boto3

# Initialize AWS clients
cloudtrail_client = boto3.client('cloudtrail')

def create_trail(name, s3_bucket_name):
    response = cloudtrail_client.create_trail(
        Name=name,
        S3BucketName=s3_bucket_name,
        IncludeGlobalServiceEvents=True,
        IsMultiRegionTrail=True,
        EnableLogFileValidation=True
    )
    return response

def start_logging(trail_name):
    response = cloudtrail_client.start_logging(Name=trail_name)
    return response

if __name__ == '__main__':
    trail_name = 'network-security-trail'
    s3_bucket_name = 'network-security-cloudtrail-logs'
    
    trail_response = create_trail(trail_name, s3_bucket_name)
    logging_response = start_logging(trail_name)
    
    print(f"CloudTrail created: {trail_response}")
    print(f"CloudTrail logging started: {logging_response}")
