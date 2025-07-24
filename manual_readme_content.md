## Authorization

Upon installing AWS Systems Manager and configuring your asset, you will want to make sure your AWS
account (preferably with Administrator privileges) has the following permissions:

- The AmazonSSMFullAccess policy is attached directly to the account
- Ability to read and write to S3 buckets

If it is preferred to use a role and Phantom is running as an EC2 instance, the **use_role**
checkbox can be checked instead. This will allow the role that is attached to the instance to be
used. Please see the [AWS EC2 and IAM
documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html)
for more information.\
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

- A new asset configuration parameter has been added in v2.0 of the app. Hence, it is requested to
  the end-user to update their existing assets and playbooks accordingly.

  - Default S3 Bucket Name: This parameter defines the default AWS S3 bucket to be used for
    writing the output of the **get file** and the **execute program** actions. For performance
    optimality, the **test connectivity** action does not validate this parameter.
