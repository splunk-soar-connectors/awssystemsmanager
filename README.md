[comment]: # "Auto-generated SOAR connector documentation"
# AWS Systems Manager

Publisher: Splunk  
Connector Version: 2.3.1  
Product Vendor: AWS  
Product Name: Systems Manager  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 5.2.0  

This app integrates with AWS Simple Systems Manager (SSM) to remotely and securely manage the configuration of any EC2 instance or on-premise machine configured for SSM

[comment]: # " File: README.md"
[comment]: # "  Copyright (c) 2019-2023 Splunk Inc."
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
**access_key** |  optional  | password | Access Key
**secret_key** |  optional  | password | Secret Key
**region** |  required  | string | Region
**default_s3_bucket** |  required  | string | Default S3 Bucket Name
**use_role** |  optional  | boolean | Use attached role when running Phantom in EC2

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

Running a shell script command will automatically write the output into an S3 bucket name of your choice or defaults the bucket name to the 'default_s3_bucket' asset congiguration parameter if no bucket name is provided. If the bucket is non-existent, this action will create the S3 bucket.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance_id** |  required  | The AWS Instance ID of where the command will run | string |  `aws instance id` 
**platform_type** |  required  | The operating system of the instance | string | 
**command** |  required  | Single command to be executed on the instance | string | 
**working_directory** |  optional  | The path to the working directory on your instance | string | 
**timeout_seconds** |  optional  | If this time is reached and the command has not already started running, it will not run | numeric | 
**comment** |  optional  | User-specified information about the command, such as a brief description of what the command should do | string | 
**output_s3_bucket_name** |  optional  | The name of the existing S3 bucket where command execution responses should be stored | string | 
**save_output_to_vault** |  optional  | Store the output of the command into the vault | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   Server 
action_result.data.\*.ResponseMetadata.HTTPHeaders.connection | string |  |   keep-alive 
action_result.data.\*.File.s3_object_key | string |  |   38ce5c4b-ab2d-4558-a575-50c660c717a2/i-09b82292b88337969/awsrunShellScript/0.awsrunShellScript/stdout 
action_result.status | string |  |   success  failed 
action_result.parameter.command | string |  |   pwd  cat file.txt 
action_result.parameter.comment | string |  |   Checking contents of parent directory 
action_result.parameter.instance_id | string |  `aws instance id`  |   i-0ea1454477403286d  i-0274f8f32148f539f 
action_result.parameter.output_s3_bucket_name | string |  |   ssm-phantom-app 
action_result.parameter.platform_type | string |  |   Linux  Windows 
action_result.parameter.save_output_to_vault | boolean |  |   True  False 
action_result.parameter.timeout_seconds | numeric |  |   30 
action_result.parameter.working_directory | string |  |   /usr/bin  /Users/Administrator/Desktop/ 
action_result.data.\*.Command.CloudWatchOutputConfig.CloudWatchLogGroupName | string |  |  
action_result.data.\*.Command.CloudWatchOutputConfig.CloudWatchOutputEnabled | boolean |  |   True  False 
action_result.data.\*.Command.InstanceIds | string |  `aws instance id`  |   i-0ea1454477403286d  i-0274f8f32148f539f 
action_result.data.\*.Command.DocumentName | string |  `aws document name`  |   AWS-RunShellScript  AWS-RunPowerShellScript 
action_result.data.\*.Command.CommandId | string |  `aws command id`  |   88e37730-5fa8-48f7-8135-26d19d77d75c  38c9d6fa-35db-42bf-b694-468bdc9c701c 
action_result.data.\*.File.output | string |  |   
Path               
----               
C:\\Windows\\system32


 
action_result.data.\*.Command.Comment | string |  |   Checking contents of parent directory 
action_result.data.\*.Command.CompletedCount | numeric |  |   0 
action_result.data.\*.Command.DeliveryTimedOutCount | numeric |  |   0 
action_result.data.\*.Command.DocumentVersion | string |  |  
action_result.data.\*.Command.ErrorCount | numeric |  |   0 
action_result.data.\*.Command.ExpiresAfter | string |  |   2019-05-14 16:17:03  2019-06-03 15:15:13 
action_result.data.\*.Command.MaxConcurrency | string |  |   50 
action_result.data.\*.Command.MaxErrors | string |  |   0 
action_result.data.\*.Command.NotificationConfig.NotificationArn | string |  |  
action_result.data.\*.Command.NotificationConfig.NotificationType | string |  |  
action_result.data.\*.Command.OutputS3BucketName | string |  |   ssm-phantom-app 
action_result.data.\*.Command.OutputS3KeyPrefix | string |  |  
action_result.data.\*.Command.Parameters.command | string |  |   pwd 
action_result.data.\*.Command.Parameters.workingDirectory | string |  |   /usr/bin 
action_result.data.\*.Command.RequestedDateTime | string |  |   2019-05-14 15:16:33  2019-06-03 13:15:13 
action_result.data.\*.Command.ServiceRole | string |  |  
action_result.data.\*.Command.Status | string |  |   Pending 
action_result.data.\*.Command.StatusDetails | string |  |   Pending 
action_result.data.\*.Command.TargetCount | numeric |  |   1 
action_result.data.\*.File.filename | string |  |   stdout 
action_result.data.\*.File.vault_id | string |  `sha1`  `vault id`  |   6f3832d6a9dd6e41533f9648052c07f2379ec6fa 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   796  728 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   application/x-amz-json-1.1 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Tue, 14 May 2019 22:16:32 GMT  Mon, 03 Jun 2019 20:15:13 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   2a92b645-b13f-4df2-862a-3ed169e20299  2e090e5f-d76c-4cab-958e-c97582ad7424 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   2a92b645-b13f-4df2-862a-3ed169e20299  2e090e5f-d76c-4cab-958e-c97582ad7424 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.created_vault_id | string |  `sha1`  |   6f3832d6a9dd6e41533f9648052c07f2379ec6fa 
action_result.summary.status | string |  |   Successfully executed program 
action_result.message | string |  |   Status: Successfully executed program, Created vault id: 6f3832d6a9dd6e41533f9648052c07f2379ec6fa 
summary.total_objects | numeric |  |   1  2 
summary.total_objects_successful | numeric |  |   1  0 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2021-06-07 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='}   

## action: 'get file'
Retrieve a file from an AWS instance and save it to the vault

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance_id** |  required  | The AWS Instance ID of where to grab the file from | string |  `aws instance id` 
**platform_type** |  required  | The operating system of the instance | string | 
**file_path** |  required  | Full path of the file to download (include filename) | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   Server 
action_result.data.\*.ResponseMetadata.HTTPHeaders.connection | string |  |   keep-alive 
action_result.status | string |  |   success  failed 
action_result.parameter.file_path | string |  |   /home/ec2-user/saver.py 
action_result.parameter.instance_id | string |  `aws instance id`  |   i-0ea1454477403286d 
action_result.parameter.platform_type | string |  |   Linux 
action_result.data.\*.Command.CloudWatchOutputConfig.CloudWatchLogGroupName | string |  |  
action_result.data.\*.Command.CloudWatchOutputConfig.CloudWatchOutputEnabled | boolean |  |   True  False 
action_result.data.\*.Command.CommandId | string |  |   ca9bf311-0cc1-435c-ad87-cd55492f5bff 
action_result.data.\*.Command.Comment | string |  |  
action_result.data.\*.Command.CompletedCount | numeric |  |   0 
action_result.data.\*.Command.DeliveryTimedOutCount | numeric |  |   0 
action_result.data.\*.Command.DocumentName | string |  `aws document name`  |   AWS-RunShellScript 
action_result.data.\*.Command.DocumentVersion | string |  |  
action_result.data.\*.Command.ErrorCount | numeric |  |   0 
action_result.data.\*.Command.ExpiresAfter | string |  |   2019-06-13 17:03:51 
action_result.data.\*.Command.InstanceIds | string |  |   i-0ea1454477403286d 
action_result.data.\*.Command.MaxConcurrency | string |  |   50 
action_result.data.\*.Command.MaxErrors | string |  |   0 
action_result.data.\*.Command.NotificationConfig.NotificationArn | string |  |  
action_result.data.\*.Command.NotificationConfig.NotificationType | string |  |  
action_result.data.\*.Command.OutputS3BucketName | string |  |   ssm-phantom-app 
action_result.data.\*.Command.OutputS3KeyPrefix | string |  |  
action_result.data.\*.Command.Parameters.commands | string |  |   cat /home/ec2-user/saver.py | base64 
action_result.data.\*.Command.RequestedDateTime | string |  |   2019-06-13 15:03:51 
action_result.data.\*.Command.ServiceRole | string |  |  
action_result.data.\*.Command.Status | string |  |   Pending 
action_result.data.\*.Command.StatusDetails | string |  |   Pending 
action_result.data.\*.Command.TargetCount | numeric |  |   1 
action_result.data.\*.File.filename | string |  |   saver.py 
action_result.data.\*.File.s3_object_key | string |  |   ca9bf311-0cc1-435c-ad87-cd55492f5bff/i-0ea1454477403286d/awsrunShellScript/0.awsrunShellScript/stdout 
action_result.data.\*.File.vault_id | string |  `sha1`  `vault id`  |   3fa5db539d7bceec01ac4c100481aa5682766d33 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   756 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   application/x-amz-json-1.1 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Thu, 13 Jun 2019 22:03:51 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   162d4090-5f0f-451e-bbc2-c5ab17a51aa4 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   162d4090-5f0f-451e-bbc2-c5ab17a51aa4 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.created_vault_id | string |  `sha1`  |   3fa5db539d7bceec01ac4c100481aa5682766d33 
action_result.summary.status | string |  |   Successfully downloaded file into the vault 
action_result.message | string |  |   Status: Successfully downloaded file into the vault, Created vault id: 3fa5db539d7bceec01ac4c100481aa5682766d33 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2021-06-07 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='}   

## action: 'run document'
Runs command using a public or custom SSM Document on one or more managed instances

Type: **generic**  
Read only: **False**

The output of the action will be stored into an S3 bucket, if provided. If the bucket is non-existent, this action will create the S3 bucket.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance_id** |  required  | The AWS Instance ID of where the command will run | string |  `aws instance id` 
**document_name** |  required  | The name of the Systems Manager document to run. This can be a public document or a custom document | string |  `aws document name` 
**document_hash** |  required  | The Sha256 or Sha1 hash created by the system when the document was created | string |  `sha256`  `sha1` 
**parameters** |  required  | JSON object. The required and optional parameters specified in the document being run. Example: {"commands": ["ls"]} | string | 
**working_directory** |  optional  | The path to the working directory on your instance | string | 
**timeout_seconds** |  optional  | If this time is reached and the command has not already started running, it will not run | numeric | 
**comment** |  optional  | User-specified information about the command, such as a brief description of what the command should do | string | 
**output_s3_bucket_name** |  optional  | The name of the S3 bucket where command execution responses should be stored | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   Server 
action_result.data.\*.ResponseMetadata.HTTPHeaders.connection | string |  |   keep-alive 
action_result.status | string |  |   success  failed 
action_result.parameter.comment | string |  |   Run Doc Action 
action_result.parameter.document_hash | string |  `sha256`  `sha1`  |   99749de5e62f71e5ebe9a55c2321e2c394796afe7208cff048696541e6f6771e 
action_result.parameter.document_name | string |  `aws document name`  |   AWS-RunShellScript 
action_result.parameter.instance_id | string |  `aws instance id`  |   i-0ea1454477403286d 
action_result.parameter.output_s3_bucket_name | string |  |   ssm-phantom-app 
action_result.parameter.parameters | string |  |   {"commands": ["ls"]} 
action_result.parameter.timeout_seconds | numeric |  |   30 
action_result.parameter.working_directory | string |  |   /usr/bin 
action_result.data.\*.Command.CloudWatchOutputConfig.CloudWatchLogGroupName | string |  |  
action_result.data.\*.Command.CloudWatchOutputConfig.CloudWatchOutputEnabled | boolean |  |   True  False 
action_result.data.\*.Command.CommandId | string |  `aws command id`  |   3bf78866-3492-4ffa-9fff-62215f8c7b13 
action_result.data.\*.Command.Comment | string |  |   Run Doc Action 
action_result.data.\*.Command.CompletedCount | numeric |  |   0 
action_result.data.\*.Command.DeliveryTimedOutCount | numeric |  |   0 
action_result.data.\*.Command.DocumentName | string |  `aws document name`  |   AWS-RunShellScript 
action_result.data.\*.Command.DocumentVersion | string |  |  
action_result.data.\*.Command.ErrorCount | numeric |  |   0 
action_result.data.\*.Command.ExpiresAfter | string |  |   2019-05-15 15:07:26 
action_result.data.\*.Command.InstanceIds | string |  `aws instance id`  |   i-0ea1454477403286d 
action_result.data.\*.Command.MaxConcurrency | string |  |   50 
action_result.data.\*.Command.MaxErrors | string |  |   0 
action_result.data.\*.Command.NotificationConfig.NotificationArn | string |  |  
action_result.data.\*.Command.NotificationConfig.NotificationType | string |  |  
action_result.data.\*.Command.OutputS3BucketName | string |  |   ssm-phantom-app 
action_result.data.\*.Command.OutputS3KeyPrefix | string |  |  
action_result.data.\*.Command.Parameters.commands | string |  |   ls 
action_result.data.\*.Command.Parameters.workingDirectory | string |  |   /usr/bin 
action_result.data.\*.Command.RequestedDateTime | string |  |   2019-05-15 14:06:56 
action_result.data.\*.Command.ServiceRole | string |  |  
action_result.data.\*.Command.Status | string |  |   Pending 
action_result.data.\*.Command.StatusDetails | string |  |   Pending 
action_result.data.\*.Command.TargetCount | numeric |  |   1 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   768 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   application/x-amz-json-1.1 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Wed, 15 May 2019 21:06:56 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   406e48bd-0acb-49a9-8755-3ac2f8f1de58 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   406e48bd-0acb-49a9-8755-3ac2f8f1de58 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.status | string |  |   Successfully sent command 
action_result.message | string |  |   Status: Successfully sent command 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2021-06-07 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='}   

## action: 'list commands'
Lists the commands ran by users of the AWS account

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**command_id** |  optional  | If provided, lists only the specified command | string |  `aws command id` 
**instance_id** |  optional  | Lists commands issued against this instance ID | string |  `aws instance id` 
**max_results** |  optional  | The maximum number of items to return for this call | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.Commands.\*.Targets.\*.Key | string |  |   InstanceIds 
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   Server 
action_result.data.\*.ResponseMetadata.HTTPHeaders.connection | string |  |   keep-alive 
action_result.status | string |  |   success  failed 
action_result.parameter.command_id | string |  `aws command id`  |   8fbd52dd-ddc9-4206-a49f-810ec50e929e 
action_result.parameter.instance_id | string |  `aws instance id`  |   i-0ea1454477403286d 
action_result.parameter.max_results | numeric |  |   3 
action_result.data.\*.Commands.\*.CloudWatchOutputConfig.CloudWatchLogGroupName | string |  |  
action_result.data.\*.Commands.\*.CloudWatchOutputConfig.CloudWatchOutputEnabled | boolean |  |   True  False 
action_result.data.\*.Commands.\*.CommandId | string |  `aws command id`  |   c31c1788-5840-4d85-9eaa-58f851572140  8fbd52dd-ddc9-4206-a49f-810ec50e929e 
action_result.data.\*.Commands.\*.Comment | string |  |   Checking contents of directory 
action_result.data.\*.Commands.\*.CompletedCount | numeric |  |   1 
action_result.data.\*.Commands.\*.DeliveryTimedOutCount | numeric |  |   0 
action_result.data.\*.Commands.\*.DocumentName | string |  `aws document name`  |   AWS-RunShellScript 
action_result.data.\*.Commands.\*.DocumentVersion | string |  |  
action_result.data.\*.Commands.\*.ErrorCount | numeric |  |   0 
action_result.data.\*.Commands.\*.ExpiresAfter | string |  |   2019-05-22 03:41:52  2019-05-22 16:47:09 
action_result.data.\*.Commands.\*.InstanceIds | string |  `aws instance id`  |   i-0ea1454477403286d 
action_result.data.\*.Commands.\*.MaxConcurrency | string |  |   50 
action_result.data.\*.Commands.\*.MaxErrors | string |  |   0 
action_result.data.\*.Commands.\*.NotificationConfig.NotificationArn | string |  |  
action_result.data.\*.Commands.\*.NotificationConfig.NotificationType | string |  |  
action_result.data.\*.Commands.\*.OutputS3BucketName | string |  |   ssm-phantom-app 
action_result.data.\*.Commands.\*.OutputS3KeyPrefix | string |  |  
action_result.data.\*.Commands.\*.Parameters.Operation | string |  |   Install 
action_result.data.\*.Commands.\*.Parameters.commands | string |  |   ps aux  pwd 
action_result.data.\*.Commands.\*.Parameters.executionTimeout | string |  |   3600 
action_result.data.\*.Commands.\*.Parameters.workingDirectory | string |  |   /home/centos  /usr/bin 
action_result.data.\*.Commands.\*.RequestedDateTime | string |  |   2019-05-22 01:41:52  2019-05-22 15:46:39 
action_result.data.\*.Commands.\*.ServiceRole | string |  |  
action_result.data.\*.Commands.\*.Status | string |  |   Success 
action_result.data.\*.Commands.\*.StatusDetails | string |  |   Success 
action_result.data.\*.Commands.\*.TargetCount | numeric |  |   1 
action_result.data.\*.NextToken | string |  |   AAEAAVExdeRKApBXO9ofnDcyXchyXgZ7RPfufGR1OtIvHtvJAAAAAFzlzDKccrMg7XM4Q8+saHge+Un5krslphWfAQkDdtLdInAKkv9SeBDQa38jCk3CGF7CeCS0ot5kmBwynEMvrdPFnOk4zio6CTbfdQovrUl4ayo+0aPYGYQMEMS8VRDZ5g0UzKE+Gh67dIJdL2xklSRpZIduR4dYymA5GutXj5mR2TT0z4yxi4OXuCRabc7epi2B8cqn+AL1FrHB4DqPYOT7y6HOXhUWE+uuN2m0X4DPTZD0q/LgV8XrpuN0GM3sc5SxJsuZje11oEhkm+WgsY23HL68ChRXvsdQGIS1ot9d5hGvNbwnMWCb0DKnMITDpEVQ6QIdg5qXmbXoniYgXGmatLg/0k+HsS5irMV8ejpR68aullGh9XTuhM+23iZzYrdtlTieP/WspQ4IcRKhR9otaTi0t/OS8Cb9UfMcRqA7N+swY67PQr68aOjbbSw3J6BQ6rYFQoVvryHxFsxdmhwDj8Ho4Y2FdyfcxkUqgOCAvtfwStOEcch/Ei2hcz7e1B8mYmGy8l7xSH/sfCmppsJIqCiVllOKevDfwSxP1iSi/BD5+8Xgrvcl14PCh5iiG4Y2CVnTs7Bzf2GOae5/J232aMIumkr7Q6OxSAoNWcTKhebjvoyssCaZjCLGWcV7A/+yTPiI+S+gS3QaReinjAAGupTcgkG3UbsmyeQMRU4ttF1okfmUsiAW1/XOVxdliWCchW2Pmm7nkNm+OhkF0rjeRx9LcQkXySInHiHCq7nyG391/ZHn1NKun/U40/tY4qSjuT/cl5GTlnX/AJShGJ4wAGqC3O0sPyKKnjCNM6sttTWqfCX7/aUNdsPOdwWSxfBrlk3Xdm8QpwrqfSvr0EB0SNrrrGG5w4KzVmHSZ+Y+v5Vc+mEfNsrBD22/ZX/ySOK0EVq7etlQUrXA4pzGTHwxt1kmMWOrqz5M1tpX6Rrqao04XURpyH5cGxhbNC1JpKdDo9G+kX11y1dO4F15GAhayCQikSuWJIH304nn2tDrldtYzyR02D52zu5l9bTp98cCC1AfHtfooFGrbKRusYFH9B8mSlaQLgRNju74Z9hQ//Gr8g== 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   3321  786 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   application/x-amz-json-1.1 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Wed, 22 May 2019 22:24:50 GMT  Wed, 22 May 2019 23:15:56 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   13a8b8fa-18dd-493f-b160-3d024f81d60e  4e59e72f-4b08-4b4d-b804-95c261306282 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   13a8b8fa-18dd-493f-b160-3d024f81d60e  4e59e72f-4b08-4b4d-b804-95c261306282 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.num_commands | numeric |  |   43  1 
action_result.message | string |  |   Num commands: 43  Num commands: 1 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2021-06-07 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='}   

## action: 'list documents'
Lists one or more of the Systems Manager documents

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** |  optional  | The name of the document to search for (case sensitive) | string |  `aws document name` 
**owner** |  optional  | The owner of the document to search for | string | 
**platform_type** |  optional  | The OS platform type that the document can execute on (i.e. Windows, Linux) | string | 
**document_type** |  optional  | The type of document | string | 
**max_results** |  optional  | The maximum number of items to return for this call | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.document_type | string |  |   Command 
action_result.parameter.max_results | numeric |  |   5 
action_result.parameter.name | string |  `aws document name`  |   AWS 
action_result.parameter.owner | string |  |   Amazon 
action_result.parameter.platform_type | string |  |   Linux 
action_result.data.\*.DocumentFormat | string |  |   JSON 
action_result.data.\*.DocumentType | string |  |   Command 
action_result.data.\*.DocumentVersion | string |  |   1 
action_result.data.\*.Name | string |  `aws document name`  |   AWS-ConfigureAWSPackage 
action_result.data.\*.Owner | string |  |   Amazon 
action_result.data.\*.PlatformTypes | string |  |   Linux 
action_result.data.\*.SchemaVersion | string |  |   2.0 
action_result.data.\*.TargetType | string |  |   /AWS::EC2::Instance 
action_result.summary.num_documents | numeric |  |   5 
action_result.message | string |  |   Num documents: 5 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2021-06-07 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='}   

## action: 'get parameter'
Get information about a parameter by using the parameter name

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** |  required  | The name of the parameter that you want to query | string |  `aws parameter name` 
**with_decryption** |  optional  | Check to decrypt values of secure string parameters. This flag is ignored for String and StringList parameter types | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   Server 
action_result.data.\*.ResponseMetadata.HTTPHeaders.connection | string |  |   keep-alive 
action_result.status | string |  |   success  failed 
action_result.parameter.name | string |  `aws parameter name`  |   test-parameter 
action_result.parameter.with_decryption | boolean |  |   True  False 
action_result.data.\*.Parameter.ARN | string |  |   arn:aws:ssm:us-east-1:849257271967:parameter/test-parameter 
action_result.data.\*.Parameter.LastModifiedDate | string |  |   2019-05-08 15:53:29 
action_result.data.\*.Parameter.Name | string |  `aws parameter name`  |   test-parameter 
action_result.data.\*.Parameter.Type | string |  |   String 
action_result.data.\*.Parameter.Value | string |  |   testing values 
action_result.data.\*.Parameter.Version | numeric |  |   1 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   206 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   application/x-amz-json-1.1 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Fri, 17 May 2019 18:34:15 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   1033d084-54da-4854-830a-cc498108fe19 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   1033d084-54da-4854-830a-cc498108fe19 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.status | string |  |   Successfully retrieved parameter 
action_result.message | string |  |   Status: Successfully retrieved parameter 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2021-06-07 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='}   

## action: 'add parameter'
Adds a parameter to the AWS account's Parameter Store

Type: **generic**  
Read only: **False**

<b>Parameter Naming Constraints:</b><ul><li>Parameter names are case sensitive.</li><li>A parameter name must be unique within an AWS Region</li><li>A parameter name can't be prefixed with "aws" or "ssm" (case-insensitive).</li><li>Parameter names can include only the following symbols and letters: a-zA-Z0-9_.-/</li><li>A parameter name can't include spaces.</li><li>Parameter hierarchies are limited to a maximum depth of fifteen levels.</li><li>The maximum length for the fully qualified parameter name is 1011 characters.</li></ul>

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** |  required  | The fully qualified name of the parameter that you want to add to the system. Please refer to app documentation page for naming restrictions | string |  `aws parameter name` 
**description** |  optional  | Information about the parameter that you want to add to the system. Optional but recommended | string | 
**value** |  required  | The parameter value that you want to add to the system. Standard parameters have a value limit of 4 KB. Advanced parameters have a value limit of 8 KB | string | 
**type** |  required  | The type of parameter that you want to add to the system. Items in StringList must be separated by a comma (,). SecureString parameters must use an AWS KMS Key ID | string | 
**key_id** |  optional  | The KMS Key ID that you want to use to encrypt a SecureString parameter. Defaults to the AWS KMS key automatically assigned to your AWS account if no key ID is provided | string | 
**overwrite** |  optional  | Overwrite an existing parameter | boolean | 
**allowed_pattern** |  optional  | A regular expression used to validate the parameter value. For example, for String types with values restricted to numbers, you can specify the following: AllowedPattern=^d+$ | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   Server 
action_result.data.\*.ResponseMetadata.HTTPHeaders.connection | string |  |   keep-alive 
action_result.status | string |  |   success  failed 
action_result.parameter.allowed_pattern | string |  |   ^[a-z0-9_\\-]+$ 
action_result.parameter.description | string |  |   parameter for testing 
action_result.parameter.key_id | string |  |   alias/aws/ssm 
action_result.parameter.name | string |  `aws parameter name`  |   phantom 
action_result.parameter.overwrite | boolean |  |   True  False 
action_result.parameter.type | string |  |   SecureString 
action_result.parameter.value | string |  |   thephantom 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   13 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   application/x-amz-json-1.1 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Tue, 21 May 2019 16:46:04 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   db8eb7d9-c532-4929-aa20-f1d7c1703ce1 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   db8eb7d9-c532-4929-aa20-f1d7c1703ce1 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.data.\*.Version | numeric |  |   1 
action_result.summary.status | string |  |   Successfully added parameter 
action_result.message | string |  |   Status: Successfully added parameter 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2021-06-07 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='}   

## action: 'describe instance'
Describes your AWS instance, including the instance's platform type

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**instance_id** |  required  | The AWS instance ID | string |  `aws instance id` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.ResponseMetadata.HTTPHeaders.server | string |  |   Server 
action_result.data.\*.ResponseMetadata.HTTPHeaders.connection | string |  |   keep-alive 
action_result.data.\*.InstanceInformationList.\*.LastSuccessfulAssociationExecutionDate | string |  |   2021-03-01 05:01:53 
action_result.data.\*.InstanceInformationList.\*.AssociationStatus | string |  |   Success 
action_result.data.\*.InstanceInformationList.\*.LastAssociationExecutionDate | string |  |   2021-03-01 05:01:53 
action_result.data.\*.InstanceInformationList.\*.AssociationOverview.DetailedStatus | string |  |   Success 
action_result.data.\*.InstanceInformationList.\*.AssociationOverview.InstanceAssociationStatusAggregatedCount.Success | numeric |  |   4 
action_result.status | string |  |   success  failed 
action_result.parameter.instance_id | string |  `aws instance id`  |   i-0274f8f32148f539f 
action_result.data.\*.InstanceInformationList.\*.AgentVersion | string |  |   2.3.444.0 
action_result.data.\*.InstanceInformationList.\*.ComputerName | string |  |   EC2AMAZ-QFKJV94.WORKGROUP 
action_result.data.\*.InstanceInformationList.\*.IPAddress | string |  `ip`  |   172.31.84.173 
action_result.data.\*.InstanceInformationList.\*.InstanceId | string |  `aws instance id`  |   i-0274f8f32148f539f 
action_result.data.\*.InstanceInformationList.\*.IsLatestVersion | boolean |  |   True  False 
action_result.data.\*.InstanceInformationList.\*.LastPingDateTime | string |  |   2019-06-12 13:22:04 
action_result.data.\*.InstanceInformationList.\*.PingStatus | string |  |   Online 
action_result.data.\*.InstanceInformationList.\*.PlatformName | string |  |   Microsoft Windows Server 2019 Datacenter 
action_result.data.\*.InstanceInformationList.\*.PlatformType | string |  |   Windows 
action_result.data.\*.InstanceInformationList.\*.PlatformVersion | string |  |   10.0.17763 
action_result.data.\*.InstanceInformationList.\*.ResourceType | string |  |   EC2Instance 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string |  |   389 
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string |  |   application/x-amz-json-1.1 
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string |  |   Wed, 12 Jun 2019 20:22:16 GMT 
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string |  |   351a30e4-874f-4314-962e-e7c133b460e2 
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric |  |   200 
action_result.data.\*.ResponseMetadata.RequestId | string |  |   351a30e4-874f-4314-962e-e7c133b460e2 
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric |  |   0 
action_result.summary.status | string |  |   Successfully retrieved instance information 
action_result.message | string |  |   Status: Successfully retrieved instance information 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2021-06-07 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} 