import boto3

# Initialize AWS clients
kinesis_client = boto3.client('kinesis')

def create_stream(name, shard_count):
    response = kinesis_client.create_stream(
        StreamName=name,
        ShardCount=shard_count
    )
    return response

if __name__ == '__main__':
    stream_name = 'network-security-stream'
    shard_count = 1
    
    stream_response = create_stream(stream_name, shard_count)
    
    print(f"Kinesis stream created: {stream_response}")
