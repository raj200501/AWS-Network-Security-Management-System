import boto3
import json

# Initialize AWS clients
waf_client = boto3.client('waf')

def create_web_acl(name):
    response = waf_client.create_web_acl(
        Name=name,
        MetricName=name,
        DefaultAction={'Type': 'ALLOW'},
        VisibilityConfig={
            'SampledRequestsEnabled': True,
            'CloudWatchMetricsEnabled': True,
            'MetricName': name
        }
    )
    return response

def create_ip_set(name):
    response = waf_client.create_ip_set(
        Name=name,
        Scope='REGIONAL',
        IPAddressVersion='IPV4',
        Addresses=[]
    )
    return response

def associate_web_acl_with_resource(web_acl_arn, resource_arn):
    response = waf_client.associate_web_acl(
        WebACLArn=web_acl_arn,
        ResourceArn=resource_arn
    )
    return response

if __name__ == '__main__':
    web_acl_name = 'network-security-web-acl'
    ip_set_name = 'network-security-ip-set'
    resource_arn = 'arn:aws:apigateway:region::/restapis/api-id/stages/prod'
    
    web_acl_response = create_web_acl(web_acl_name)
    ip_set_response = create_ip_set(ip_set_name)
    
    web_acl_arn = web_acl_response['Summary']['ARN']
    association_response = associate_web_acl_with_resource(web_acl_arn, resource_arn)
    
    print(f"Web ACL created: {web_acl_response}")
    print(f"IP Set created: {ip_set_response}")
    print(f"Web ACL associated with resource: {association_response}")
