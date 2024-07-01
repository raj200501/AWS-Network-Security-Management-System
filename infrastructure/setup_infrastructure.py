import boto3

# Initialize AWS clients
cloudformation_client = boto3.client('cloudformation')

def create_stack(stack_name, template_body):
    response = cloudformation_client.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Capabilities=['CAPABILITY_NAMED_IAM']
    )
    return response

if __name__ == '__main__':
    stack_name = 'network-security-stack'
    with open('infrastructure/cloudformation_template.yaml', 'r') as template_file:
        template_body = template_file.read()
    
    response = create_stack(stack_name, template_body)
    print(f"Stack creation initiated: {response}")
