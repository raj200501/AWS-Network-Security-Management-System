import boto3
import json

# Initialize AWS clients
config_client = boto3.client('config')
sns_client = boto3.client('sns')

# SNS topic for compliance alerts
sns_topic_arn = 'arn:aws:sns:region:account-id:network-security-compliance-alerts'

def check_compliance():
    response = config_client.get_compliance_summary_by_config_rule()
    non_compliant_rules = [
        rule for rule in response['ComplianceSummaryByConfigRules']
        if rule['ComplianceSummary']['NonCompliantResourceCount']['TotalCount'] > 0
    ]
    return non_compliant_rules

def lambda_handler(event, context):
    non_compliant_rules = check_compliance()
    
    if non_compliant_rules:
        alert_message = f"Non-compliant rules detected: {json.dumps(non_compliant_rules)}"
        sns_client.publish(TopicArn=sns_topic_arn, Message=alert_message)
        print(alert_message)

    return {'statusCode': 200, 'body': json.dumps('Compliance check completed')}
