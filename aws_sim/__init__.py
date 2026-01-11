"""Local AWS service simulators for NSMS.

These modules provide deterministic, in-memory simulations of AWS services used
by the original architecture. They allow tests and local runs to exercise AWS-
like behaviors without credentials.
"""

from aws_sim.kinesis import KinesisStream, KinesisRecord
from aws_sim.lambda_runtime import LambdaRuntime, LambdaFunction
from aws_sim.sns import SnsTopic, SnsMessage
from aws_sim.dynamodb import DynamoTable, DynamoItem
from aws_sim.s3 import S3Bucket, S3Object
from aws_sim.cloudtrail import CloudTrailRecorder, CloudTrailEvent
from aws_sim.config_rules import ConfigRule, ConfigEvaluator
from aws_sim.iam import IamPolicy, IamRole, PolicyDecision
from aws_sim.guardduty import GuardDutyDetector, GuardDutyFinding
from aws_sim.securityhub import SecurityHub, SecurityHubFinding
from aws_sim.cloudwatch import CloudWatchMetrics, CloudWatchAlarm, MetricDatum, AlarmState
from aws_sim.kms import KmsKey, KeyMetadata
from aws_sim.sts import StsService, SessionCredentials
from aws_sim.metadata import ResourceMetadata, ResourceTags
from aws_sim.resource_policies import ResourcePolicy, ResourcePolicyStatement
from aws_sim.cloudformation import CloudFormationService, CloudFormationStack, StackTemplate
from aws_sim.vpc import VpcService, Vpc, Subnet, SecurityGroup, SecurityGroupRule, RouteTable, Route
from aws_sim.waf import WafWebAcl, WafRule, WafRequest, WafDecision, IpSet, StringMatchStatement, RateBasedStatement
from aws_sim.organizations import OrganizationsService, Account, OrganizationalUnit, ServiceControlPolicy
from aws_sim.inspector import InspectorService, AssessmentTemplate, AssessmentRun, InspectorFinding
from aws_sim.firehose import FirehoseDeliveryStream, FirehoseRecord
from aws_sim.ecs import EcsService, Cluster, Service, TaskDefinition, Task, ContainerDefinition
from aws_sim.elasticloadbalancing import ElbService, LoadBalancer, Listener, TargetGroup, Target
from aws_sim.rds import RdsService, DbInstance, DbSnapshot

__all__ = [
    "KinesisStream",
    "KinesisRecord",
    "LambdaRuntime",
    "LambdaFunction",
    "SnsTopic",
    "SnsMessage",
    "DynamoTable",
    "DynamoItem",
    "S3Bucket",
    "S3Object",
    "CloudTrailRecorder",
    "CloudTrailEvent",
    "ConfigRule",
    "ConfigEvaluator",
    "IamPolicy",
    "IamRole",
    "PolicyDecision",
    "GuardDutyDetector",
    "GuardDutyFinding",
    "SecurityHub",
    "SecurityHubFinding",
    "CloudWatchMetrics",
    "CloudWatchAlarm",
    "MetricDatum",
    "AlarmState",
    "KmsKey",
    "KeyMetadata",
    "StsService",
    "SessionCredentials",
    "ResourceMetadata",
    "ResourceTags",
    "ResourcePolicy",
    "ResourcePolicyStatement",
    "CloudFormationService",
    "CloudFormationStack",
    "StackTemplate",
    "VpcService",
    "Vpc",
    "Subnet",
    "SecurityGroup",
    "SecurityGroupRule",
    "RouteTable",
    "Route",
    "WafWebAcl",
    "WafRule",
    "WafRequest",
    "WafDecision",
    "IpSet",
    "StringMatchStatement",
    "RateBasedStatement",
    "OrganizationsService",
    "Account",
    "OrganizationalUnit",
    "ServiceControlPolicy",
    "InspectorService",
    "AssessmentTemplate",
    "AssessmentRun",
    "InspectorFinding",
    "FirehoseDeliveryStream",
    "FirehoseRecord",
    "EcsService",
    "Cluster",
    "Service",
    "TaskDefinition",
    "Task",
    "ContainerDefinition",
    "ElbService",
    "LoadBalancer",
    "Listener",
    "TargetGroup",
    "Target",
    "RdsService",
    "DbInstance",
    "DbSnapshot",
]
