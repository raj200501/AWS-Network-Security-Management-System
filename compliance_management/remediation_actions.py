import boto3
import json

# Initialize AWS clients
config_client = boto3.client('config')
sns_client = boto3.client('sns')

# SNS topic for remediation alerts
sns_topic_arn = 'arn:aws:sns:region:account-id:network-security-remediation-alerts'

def remediate_non_compliant_resources(non_compliant_rules):
    for rule in non_compliant_rules:
        rule_name = rule['ConfigRuleName']
        response = config_client.get_compliance_details_by_config_rule(ConfigRuleName=rule_name)
        
        for resource in response['EvaluationResults']:
            resource_id = resource['EvaluationResultIdentifier']['EvaluationResultQualifier']['ResourceId']
            # Example remediation action: stop the instance
            ec2_client = boto3.client('ec2')
            ec2_client.stop_instances(InstanceIds=[resource_id])
            sns_client.publish(TopicArn=sns_topic_arn, Message=f"Stopped instance: {resource_id}")
            print(f"Remediated non-compliant resource: {resource_id}")

def lambda_handler(event, context):
    non_compliant_rules = event['non_compliant_rules']
    remediate_non_compliant_resources(non_compliant_rules)
    return {'statusCode': 200, 'body': json.dumps('Remediation actions completed')}
