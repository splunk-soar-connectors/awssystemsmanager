[comment]: # "Auto-generated SOAR connector documentation"
# AWS Systems Manager

Publisher: Splunk  
Connector Version: 2\.3\.0  
Product Vendor: AWS  
Product Name: Systems Manager  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.1\.0  

This app integrates with AWS Simple Systems Manager \(SSM\) to remotely and securely manage the configuration of any EC2 instance or on\-premise machine configured for SSM

[comment]: # " File: README.md"
[comment]: # "  Copyright (c) 2019-2022 Splunk Inc."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
## Authorization

Upon installing AWS Systems Manager and configuring your asset, you will want to make sure your AWS
account (preferably with Administrator privileges) has the following permissions:  

-   The AmazonSSMFullAccess policy is attached directly to the account
-   Ability to read and write to S3 buckets

If it is preferred to use a role and Phantom is running as an EC2 instance, the **use_role**
checkbox can be checked instead. This will allow the role that is attached to the instance to be
used. Please see the [AWS EC2 and IAM
documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html)
for more information.  
By default, AWS Systems Manager does not have permission to perform actions on your instances. You
must make sure to attach the AmazonEC2RoleforSSM IAM policy to the instance that you want to manage
with SSM. For more information on setting up your account and instances with SSM privileges, visit
the [AWS tutorial](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/tutorial_run_command.html) .

## Assumed Role Credentials

The optional **credentials** action parameter consists of temporary **assumed role** credentials
that will be used to perform the action instead of those that are configured in the **asset** . The
parameter is not designed to be configured manually but should instead be used in conjunction with
the Phantom AWS Security Token Service app. The output of the **assume_role** action of the STS app
with data path **assume_role\_\<number>:action_result.data.\*.Credentials** consists of a dictionary
containing the **AccessKeyId** , **SecretAccessKey** , **SessionToken** and **Expiration** key/value
pairs. This dictionary can be passed directly into the credentials parameter in any of the following
actions within a playbook. For more information, please see the [AWS Identity and Access Management
documentation](https://docs.aws.amazon.com/iam/index.html) .

## Playbook Backward Compatibility

-   A new asset configuration parameter has been added in v2.0 of the app. Hence, it is requested to
    the end-user to update their existing assets and playbooks accordingly.

      

    -   Default S3 Bucket Name: This parameter defines the default AWS S3 bucket to be used for
        writing the output of the **get file** and the **execute program** actions. For performance
        optimality, the **test connectivity** action does not validate this parameter.


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Systems Manager asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**access\_key** |  optional  | password | Access Key
**secret\_key** |  optional  | password | Secret Key
**region** |  required  | string | Region
**default\_s3\_bucket** |  required  | string | Default S3 Bucket Name
**use\_role** |  optional  | boolean | Use attached role when running Phantom in EC2

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[execute program](#action-execute-program) - Runs shell script command on a managed instance  
[get file](#action-get-file) - Retrieve a file from an AWS instance and save it to the vault  
[run document](#action-run-document) - Runs command using a public or custom SSM Document on one or more managed instances  
[list commands](#action-list-commands) - Lists the commands ran by users of the AWS account  
[list documents](#action-list-documents) - Lists one or more of the Systems Manager documents  
[get parameter](#action-get-parameter) - Get information about a parameter by using the parameter name  
[add parameter](#action-add-parameter) - Adds a parameter to the AWS account's Parameter Store  
[describe instance](#action-describe-instance) - Describes your AWS instance, including the instance's platform type  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'execute program'
Runs shell script command on a managed instance

Type: **generic**  
Read only: **False**

Running a shell script command will automatically write the output into an S3 bucket name of your choice or defaults the bucket name to the 'default\_s3\_bucket' asset congiguration parameter if no bucket name is provided\. If the bucket is non\-existent, this action will create the S3 bucket\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance\_id** |  required  | The AWS Instance ID of where the command will run | string |  `aws instance id` 
**platform\_type** |  required  | The operating system of the instance | string | 
**command** |  required  | Single command to be executed on the instance | string | 
**working\_directory** |  optional  | The path to the working directory on your instance | string | 
**timeout\_seconds** |  optional  | If this time is reached and the command has not already started running, it will not run | numeric | 
**comment** |  optional  | User\-specified information about the command, such as a brief description of what the command should do | string | 
**output\_s3\_bucket\_name** |  optional  | The name of the existing S3 bucket where command execution responses should be stored | string | 
**save\_output\_to\_vault** |  optional  | Store the output of the command into the vault | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string | 
action\_result\.data\.\*\.File\.s3\_object\_key | string | 
action\_result\.status | string | 
action\_result\.parameter\.command | string | 
action\_result\.parameter\.comment | string | 
action\_result\.parameter\.instance\_id | string |  `aws instance id` 
action\_result\.parameter\.output\_s3\_bucket\_name | string | 
action\_result\.parameter\.platform\_type | string | 
action\_result\.parameter\.save\_output\_to\_vault | boolean | 
action\_result\.parameter\.timeout\_seconds | numeric | 
action\_result\.parameter\.working\_directory | string | 
action\_result\.data\.\*\.Command\.CloudWatchOutputConfig\.CloudWatchLogGroupName | string | 
action\_result\.data\.\*\.Command\.CloudWatchOutputConfig\.CloudWatchOutputEnabled | boolean | 
action\_result\.data\.\*\.Command\.InstanceIds | string |  `aws instance id` 
action\_result\.data\.\*\.Command\.DocumentName | string |  `aws document name` 
action\_result\.data\.\*\.Command\.CommandId | string |  `aws command id` 
action\_result\.data\.\*\.File\.output | string | 
action\_result\.data\.\*\.Command\.Comment | string | 
action\_result\.data\.\*\.Command\.CompletedCount | numeric | 
action\_result\.data\.\*\.Command\.DeliveryTimedOutCount | numeric | 
action\_result\.data\.\*\.Command\.DocumentVersion | string | 
action\_result\.data\.\*\.Command\.ErrorCount | numeric | 
action\_result\.data\.\*\.Command\.ExpiresAfter | string | 
action\_result\.data\.\*\.Command\.MaxConcurrency | string | 
action\_result\.data\.\*\.Command\.MaxErrors | string | 
action\_result\.data\.\*\.Command\.NotificationConfig\.NotificationArn | string | 
action\_result\.data\.\*\.Command\.NotificationConfig\.NotificationType | string | 
action\_result\.data\.\*\.Command\.OutputS3BucketName | string | 
action\_result\.data\.\*\.Command\.OutputS3KeyPrefix | string | 
action\_result\.data\.\*\.Command\.Parameters\.command | string | 
action\_result\.data\.\*\.Command\.Parameters\.workingDirectory | string | 
action\_result\.data\.\*\.Command\.RequestedDateTime | string | 
action\_result\.data\.\*\.Command\.ServiceRole | string | 
action\_result\.data\.\*\.Command\.Status | string | 
action\_result\.data\.\*\.Command\.StatusDetails | string | 
action\_result\.data\.\*\.Command\.TargetCount | numeric | 
action\_result\.data\.\*\.File\.filename | string | 
action\_result\.data\.\*\.File\.vault\_id | string |  `sha1`  `vault id` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.created\_vault\_id | string |  `sha1` 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'get file'
Retrieve a file from an AWS instance and save it to the vault

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance\_id** |  required  | The AWS Instance ID of where to grab the file from | string |  `aws instance id` 
**platform\_type** |  required  | The operating system of the instance | string | 
**file\_path** |  required  | Full path of the file to download \(include filename\) | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string | 
action\_result\.status | string | 
action\_result\.parameter\.file\_path | string | 
action\_result\.parameter\.instance\_id | string |  `aws instance id` 
action\_result\.parameter\.platform\_type | string | 
action\_result\.data\.\*\.Command\.CloudWatchOutputConfig\.CloudWatchLogGroupName | string | 
action\_result\.data\.\*\.Command\.CloudWatchOutputConfig\.CloudWatchOutputEnabled | boolean | 
action\_result\.data\.\*\.Command\.CommandId | string | 
action\_result\.data\.\*\.Command\.Comment | string | 
action\_result\.data\.\*\.Command\.CompletedCount | numeric | 
action\_result\.data\.\*\.Command\.DeliveryTimedOutCount | numeric | 
action\_result\.data\.\*\.Command\.DocumentName | string |  `aws document name` 
action\_result\.data\.\*\.Command\.DocumentVersion | string | 
action\_result\.data\.\*\.Command\.ErrorCount | numeric | 
action\_result\.data\.\*\.Command\.ExpiresAfter | string | 
action\_result\.data\.\*\.Command\.InstanceIds | string | 
action\_result\.data\.\*\.Command\.MaxConcurrency | string | 
action\_result\.data\.\*\.Command\.MaxErrors | string | 
action\_result\.data\.\*\.Command\.NotificationConfig\.NotificationArn | string | 
action\_result\.data\.\*\.Command\.NotificationConfig\.NotificationType | string | 
action\_result\.data\.\*\.Command\.OutputS3BucketName | string | 
action\_result\.data\.\*\.Command\.OutputS3KeyPrefix | string | 
action\_result\.data\.\*\.Command\.Parameters\.commands | string | 
action\_result\.data\.\*\.Command\.RequestedDateTime | string | 
action\_result\.data\.\*\.Command\.ServiceRole | string | 
action\_result\.data\.\*\.Command\.Status | string | 
action\_result\.data\.\*\.Command\.StatusDetails | string | 
action\_result\.data\.\*\.Command\.TargetCount | numeric | 
action\_result\.data\.\*\.File\.filename | string | 
action\_result\.data\.\*\.File\.s3\_object\_key | string | 
action\_result\.data\.\*\.File\.vault\_id | string |  `sha1`  `vault id` 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.created\_vault\_id | string |  `sha1` 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'run document'
Runs command using a public or custom SSM Document on one or more managed instances

Type: **generic**  
Read only: **False**

The output of the action will be stored into an S3 bucket, if provided\. If the bucket is non\-existent, this action will create the S3 bucket\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance\_id** |  required  | The AWS Instance ID of where the command will run | string |  `aws instance id` 
**document\_name** |  required  | The name of the Systems Manager document to run\. This can be a public document or a custom document | string |  `aws document name` 
**document\_hash** |  required  | The Sha256 or Sha1 hash created by the system when the document was created | string |  `sha256`  `sha1` 
**parameters** |  required  | JSON object\. The required and optional parameters specified in the document being run\. Example\: \{"commands"\: \["ls"\]\} | string | 
**working\_directory** |  optional  | The path to the working directory on your instance | string | 
**timeout\_seconds** |  optional  | If this time is reached and the command has not already started running, it will not run | numeric | 
**comment** |  optional  | User\-specified information about the command, such as a brief description of what the command should do | string | 
**output\_s3\_bucket\_name** |  optional  | The name of the S3 bucket where command execution responses should be stored | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string | 
action\_result\.status | string | 
action\_result\.parameter\.comment | string | 
action\_result\.parameter\.document\_hash | string |  `sha256`  `sha1` 
action\_result\.parameter\.document\_name | string |  `aws document name` 
action\_result\.parameter\.instance\_id | string |  `aws instance id` 
action\_result\.parameter\.output\_s3\_bucket\_name | string | 
action\_result\.parameter\.parameters | string | 
action\_result\.parameter\.timeout\_seconds | numeric | 
action\_result\.parameter\.working\_directory | string | 
action\_result\.data\.\*\.Command\.CloudWatchOutputConfig\.CloudWatchLogGroupName | string | 
action\_result\.data\.\*\.Command\.CloudWatchOutputConfig\.CloudWatchOutputEnabled | boolean | 
action\_result\.data\.\*\.Command\.CommandId | string |  `aws command id` 
action\_result\.data\.\*\.Command\.Comment | string | 
action\_result\.data\.\*\.Command\.CompletedCount | numeric | 
action\_result\.data\.\*\.Command\.DeliveryTimedOutCount | numeric | 
action\_result\.data\.\*\.Command\.DocumentName | string |  `aws document name` 
action\_result\.data\.\*\.Command\.DocumentVersion | string | 
action\_result\.data\.\*\.Command\.ErrorCount | numeric | 
action\_result\.data\.\*\.Command\.ExpiresAfter | string | 
action\_result\.data\.\*\.Command\.InstanceIds | string |  `aws instance id` 
action\_result\.data\.\*\.Command\.MaxConcurrency | string | 
action\_result\.data\.\*\.Command\.MaxErrors | string | 
action\_result\.data\.\*\.Command\.NotificationConfig\.NotificationArn | string | 
action\_result\.data\.\*\.Command\.NotificationConfig\.NotificationType | string | 
action\_result\.data\.\*\.Command\.OutputS3BucketName | string | 
action\_result\.data\.\*\.Command\.OutputS3KeyPrefix | string | 
action\_result\.data\.\*\.Command\.Parameters\.commands | string | 
action\_result\.data\.\*\.Command\.Parameters\.workingDirectory | string | 
action\_result\.data\.\*\.Command\.RequestedDateTime | string | 
action\_result\.data\.\*\.Command\.ServiceRole | string | 
action\_result\.data\.\*\.Command\.Status | string | 
action\_result\.data\.\*\.Command\.StatusDetails | string | 
action\_result\.data\.\*\.Command\.TargetCount | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'list commands'
Lists the commands ran by users of the AWS account

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**command\_id** |  optional  | If provided, lists only the specified command | string |  `aws command id` 
**instance\_id** |  optional  | Lists commands issued against this instance ID | string |  `aws instance id` 
**max\_results** |  optional  | The maximum number of items to return for this call | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.Commands\.\*\.Targets\.\*\.Key | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string | 
action\_result\.status | string | 
action\_result\.parameter\.command\_id | string |  `aws command id` 
action\_result\.parameter\.instance\_id | string |  `aws instance id` 
action\_result\.parameter\.max\_results | numeric | 
action\_result\.data\.\*\.Commands\.\*\.CloudWatchOutputConfig\.CloudWatchLogGroupName | string | 
action\_result\.data\.\*\.Commands\.\*\.CloudWatchOutputConfig\.CloudWatchOutputEnabled | boolean | 
action\_result\.data\.\*\.Commands\.\*\.CommandId | string |  `aws command id` 
action\_result\.data\.\*\.Commands\.\*\.Comment | string | 
action\_result\.data\.\*\.Commands\.\*\.CompletedCount | numeric | 
action\_result\.data\.\*\.Commands\.\*\.DeliveryTimedOutCount | numeric | 
action\_result\.data\.\*\.Commands\.\*\.DocumentName | string |  `aws document name` 
action\_result\.data\.\*\.Commands\.\*\.DocumentVersion | string | 
action\_result\.data\.\*\.Commands\.\*\.ErrorCount | numeric | 
action\_result\.data\.\*\.Commands\.\*\.ExpiresAfter | string | 
action\_result\.data\.\*\.Commands\.\*\.InstanceIds | string |  `aws instance id` 
action\_result\.data\.\*\.Commands\.\*\.MaxConcurrency | string | 
action\_result\.data\.\*\.Commands\.\*\.MaxErrors | string | 
action\_result\.data\.\*\.Commands\.\*\.NotificationConfig\.NotificationArn | string | 
action\_result\.data\.\*\.Commands\.\*\.NotificationConfig\.NotificationType | string | 
action\_result\.data\.\*\.Commands\.\*\.OutputS3BucketName | string | 
action\_result\.data\.\*\.Commands\.\*\.OutputS3KeyPrefix | string | 
action\_result\.data\.\*\.Commands\.\*\.Parameters\.Operation | string | 
action\_result\.data\.\*\.Commands\.\*\.Parameters\.commands | string | 
action\_result\.data\.\*\.Commands\.\*\.Parameters\.executionTimeout | string | 
action\_result\.data\.\*\.Commands\.\*\.Parameters\.workingDirectory | string | 
action\_result\.data\.\*\.Commands\.\*\.RequestedDateTime | string | 
action\_result\.data\.\*\.Commands\.\*\.ServiceRole | string | 
action\_result\.data\.\*\.Commands\.\*\.Status | string | 
action\_result\.data\.\*\.Commands\.\*\.StatusDetails | string | 
action\_result\.data\.\*\.Commands\.\*\.TargetCount | numeric | 
action\_result\.data\.\*\.NextToken | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.num\_commands | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'list documents'
Lists one or more of the Systems Manager documents

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** |  optional  | The name of the document to search for \(case sensitive\) | string |  `aws document name` 
**owner** |  optional  | The owner of the document to search for | string | 
**platform\_type** |  optional  | The OS platform type that the document can execute on \(i\.e\. Windows, Linux\) | string | 
**document\_type** |  optional  | The type of document | string | 
**max\_results** |  optional  | The maximum number of items to return for this call | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.document\_type | string | 
action\_result\.parameter\.max\_results | numeric | 
action\_result\.parameter\.name | string |  `aws document name` 
action\_result\.parameter\.owner | string | 
action\_result\.parameter\.platform\_type | string | 
action\_result\.data\.\*\.DocumentFormat | string | 
action\_result\.data\.\*\.DocumentType | string | 
action\_result\.data\.\*\.DocumentVersion | string | 
action\_result\.data\.\*\.Name | string |  `aws document name` 
action\_result\.data\.\*\.Owner | string | 
action\_result\.data\.\*\.PlatformTypes | string | 
action\_result\.data\.\*\.SchemaVersion | string | 
action\_result\.data\.\*\.TargetType | string | 
action\_result\.summary\.num\_documents | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'get parameter'
Get information about a parameter by using the parameter name

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** |  required  | The name of the parameter that you want to query | string |  `aws parameter name` 
**with\_decryption** |  optional  | Check to decrypt values of secure string parameters\. This flag is ignored for String and StringList parameter types | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string | 
action\_result\.status | string | 
action\_result\.parameter\.name | string |  `aws parameter name` 
action\_result\.parameter\.with\_decryption | boolean | 
action\_result\.data\.\*\.Parameter\.ARN | string | 
action\_result\.data\.\*\.Parameter\.LastModifiedDate | string | 
action\_result\.data\.\*\.Parameter\.Name | string |  `aws parameter name` 
action\_result\.data\.\*\.Parameter\.Type | string | 
action\_result\.data\.\*\.Parameter\.Value | string | 
action\_result\.data\.\*\.Parameter\.Version | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'add parameter'
Adds a parameter to the AWS account's Parameter Store

Type: **generic**  
Read only: **False**

<b>Parameter Naming Constraints\:</b><ul><li>Parameter names are case sensitive\.</li><li>A parameter name must be unique within an AWS Region</li><li>A parameter name can't be prefixed with "aws" or "ssm" \(case\-insensitive\)\.</li><li>Parameter names can include only the following symbols and letters\: a\-zA\-Z0\-9\_\.\-/</li><li>A parameter name can't include spaces\.</li><li>Parameter hierarchies are limited to a maximum depth of fifteen levels\.</li><li>The maximum length for the fully qualified parameter name is 1011 characters\.</li></ul>

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** |  required  | The fully qualified name of the parameter that you want to add to the system\. Please refer to app documentation page for naming restrictions | string |  `aws parameter name` 
**description** |  optional  | Information about the parameter that you want to add to the system\. Optional but recommended | string | 
**value** |  required  | The parameter value that you want to add to the system\. Standard parameters have a value limit of 4 KB\. Advanced parameters have a value limit of 8 KB | string | 
**type** |  required  | The type of parameter that you want to add to the system\. Items in StringList must be separated by a comma \(,\)\. SecureString parameters must use an AWS KMS Key ID | string | 
**key\_id** |  optional  | The KMS Key ID that you want to use to encrypt a SecureString parameter\. Defaults to the AWS KMS key automatically assigned to your AWS account if no key ID is provided | string | 
**overwrite** |  optional  | Overwrite an existing parameter | boolean | 
**allowed\_pattern** |  optional  | A regular expression used to validate the parameter value\. For example, for String types with values restricted to numbers, you can specify the following\: AllowedPattern=^d\+$ | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string | 
action\_result\.status | string | 
action\_result\.parameter\.allowed\_pattern | string | 
action\_result\.parameter\.description | string | 
action\_result\.parameter\.key\_id | string | 
action\_result\.parameter\.name | string |  `aws parameter name` 
action\_result\.parameter\.overwrite | boolean | 
action\_result\.parameter\.type | string | 
action\_result\.parameter\.value | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.Version | numeric | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'describe instance'
Describes your AWS instance, including the instance's platform type

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance\_id** |  required  | The AWS instance ID | string |  `aws instance id` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string | 
action\_result\.data\.\*\.InstanceInformationList\.\*\.LastSuccessfulAssociationExecutionDate | string | 
action\_result\.data\.\*\.InstanceInformationList\.\*\.AssociationStatus | string | 
action\_result\.data\.\*\.InstanceInformationList\.\*\.LastAssociationExecutionDate | string | 
action\_result\.data\.\*\.InstanceInformationList\.\*\.AssociationOverview\.DetailedStatus | string | 
action\_result\.data\.\*\.InstanceInformationList\.\*\.AssociationOverview\.InstanceAssociationStatusAggregatedCount\.Success | numeric | 
action\_result\.status | string | 
action\_result\.parameter\.instance\_id | string |  `aws instance id` 
action\_result\.data\.\*\.InstanceInformationList\.\*\.AgentVersion | string | 
action\_result\.data\.\*\.InstanceInformationList\.\*\.ComputerName | string | 
action\_result\.data\.\*\.InstanceInformationList\.\*\.IPAddress | string |  `ip` 
action\_result\.data\.\*\.InstanceInformationList\.\*\.InstanceId | string |  `aws instance id` 
action\_result\.data\.\*\.InstanceInformationList\.\*\.IsLatestVersion | boolean | 
action\_result\.data\.\*\.InstanceInformationList\.\*\.LastPingDateTime | string | 
action\_result\.data\.\*\.InstanceInformationList\.\*\.PingStatus | string | 
action\_result\.data\.\*\.InstanceInformationList\.\*\.PlatformName | string | 
action\_result\.data\.\*\.InstanceInformationList\.\*\.PlatformType | string | 
action\_result\.data\.\*\.InstanceInformationList\.\*\.PlatformVersion | string | 
action\_result\.data\.\*\.InstanceInformationList\.\*\.ResourceType | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials` 