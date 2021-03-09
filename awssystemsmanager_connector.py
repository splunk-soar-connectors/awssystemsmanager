# File: awssystemsmanager_connector.py
# Copyright (c) 2019-2021 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult
from phantom.vault import Vault
import phantom.rules as ph_rules

# Usage of the consts file is recommended
from awssystemsmanager_consts import *
from boto3 import client
from datetime import datetime
from botocore.config import Config
from bs4 import UnicodeDammit
import botocore.response as br
import botocore.paginate as bp
import requests
import json
import os
import sys
import tempfile
import time
import base64


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class AwsSystemsManagerConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(AwsSystemsManagerConnector, self).__init__()

        self._state = None
        self._region = None
        self._access_key = None
        self._secret_key = None
        self._default_s3_bucket = None
        self._proxy = None
        self._python_version = None

    def _sanitize_data(self, cur_obj):

        try:
            json.dumps(cur_obj)
            return cur_obj
        except:
            pass

        if isinstance(cur_obj, dict):
            new_dict = {}
            for k, v in cur_obj.items():
                if isinstance(v, br.StreamingBody):
                    content = v.read()
                    new_dict[k] = json.loads(content)
                else:
                    new_dict[k] = self._sanitize_data(v)
            return new_dict

        if isinstance(cur_obj, list):
            new_list = []
            for v in cur_obj:
                new_list.append(self._sanitize_data(v))
            return new_list

        if isinstance(cur_obj, datetime):
            return cur_obj.strftime("%Y-%m-%d %H:%M:%S")

        if isinstance(cur_obj, bp.PageIterator):
            new_dict = dict()
            try:
                for page in cur_obj:
                    new_dict.update(page)
                return new_dict
            except Exception as e:
                return { 'error': e }

        return cur_obj

    def _handle_py_ver_compat_for_input_str(self, input_str):
        """
        This method returns the encoded|original string based on the Python version.

        :param input_str: Input string to be processed
        :return: input_str (Processed input string based on following logic 'input_str - Python 3; encoded input_str - Python 2')
        """

        try:
            if input_str and self._python_version < 3:
                input_str = UnicodeDammit(input_str).unicode_markup.encode('utf-8')
        except:
            self.debug_print("Error occurred while handling python 2to3 compatibility for the input string")
        return input_str

    def _make_boto_call(self, action_result, method, paginate=False, empty_payload=False, **kwargs):

        if paginate is False:
            try:
                boto_func = getattr(self._client, method)
            except AttributeError:
                return RetVal(action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)), None)
            try:
                resp_json = boto_func(**kwargs)
                if empty_payload:
                    resp_json['Payload'] = {'body': "", 'statusCode': resp_json['StatusCode']}
            except Exception as e:
                exception_message = self._handle_py_ver_compat_for_input_str(e.args[0]).strip()
                if 'BucketAlreadyExists' in exception_message:
                    return phantom.APP_SUCCESS, None
                return RetVal(action_result.set_status(phantom.APP_ERROR, 'boto3 call to SSM failed', exception_message), None)
        else:
            try:
                paginator = self._client.get_paginator(method)
                resp_json = paginator.paginate(**kwargs)
            except Exception as e:
                return RetVal(action_result.set_status(phantom.APP_ERROR, 'boto3 call to SSM failed', e), None)

        return phantom.APP_SUCCESS, self._sanitize_data(resp_json)

    def _sanatize_dates(self, cur_obj):

        try:
            json.dumps(cur_obj)
            return cur_obj
        except:
            pass

        if isinstance(cur_obj, dict):
            new_dict = {}
            for k, v in cur_obj.items():
                new_dict[k] = self._sanatize_dates(v)
            return new_dict

        if isinstance(cur_obj, list):
            new_list = []
            for v in cur_obj:
                new_list.append(self._sanatize_dates(v))
            return new_list

        if isinstance(cur_obj, datetime):
            return cur_obj.strftime("%Y-%m-%d %H:%M:%S")

        return cur_obj

    def _make_s3_boto_call(self, action_result, method, **kwargs):

        try:
            boto_func = getattr(self._client, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)), None)

        try:
            resp_json = boto_func(**kwargs)
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, 'boto3 call to S3 failed', e), None)

        return phantom.APP_SUCCESS, resp_json

    def _create_client(self, action_result):

        boto_config = None
        if self._proxy:
            boto_config = Config(proxies=self._proxy)

        try:
            if self._access_key and self._secret_key:
                self.debug_print("Creating boto3 client with API keys")
                self._client = client(
                    'ssm',
                    region_name=self._region,
                    aws_access_key_id=self._access_key,
                    aws_secret_access_key=self._secret_key,
                    config=boto_config)
            else:
                self.debug_print("Creating boto3 client without API keys")
                self._client = client(
                    'ssm',
                    region_name=self._region,
                    config=boto_config)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Could not create boto3 client: {0}".format(e))

        return phantom.APP_SUCCESS

    def _create_s3_client(self, action_result):

        boto_config = None
        if self._proxy:
            boto_config = Config(proxies=self._proxy)

        try:

            if self._access_key and self._secret_key:

                self.debug_print("Creating boto3 client with API keys")

                self._client = client(
                        's3',
                        region_name=self._region,
                        aws_access_key_id=self._access_key,
                        aws_secret_access_key=self._secret_key,
                        config=boto_config)

            else:

                self.debug_print("Creating boto3 client without API keys")

                self._client = client(
                        's3',
                        region_name=self._region,
                        config=boto_config)

        except Exception as e:
            return self.set_status(phantom.APP_ERROR, "Could not create boto3 client: {0}".format(e))

        return phantom.APP_SUCCESS

    def _get_s3_bucket(self, action_result, output_s3_bucket_name):

        self._create_s3_client(action_result)

        ret_val, resp_json = self._make_boto_call(action_result, 'get_bucket_accelerate_configuration', Bucket=output_s3_bucket_name)

        return ret_val

    def _create_s3_bucket(self, action_result, output_s3_bucket_name):

        self._create_s3_client(action_result)

        location = {'LocationConstraint': SSM_REGION_DICT[self.get_config()['region']]}

        if not output_s3_bucket_name:
            output_s3_bucket_name = self._default_s3_bucket

        # boto3 bug
        if location['LocationConstraint'] == 'us-east-1':
            ret_val, resp_json = self._make_boto_call(action_result, 'create_bucket', Bucket=output_s3_bucket_name)
        else:
            ret_val, resp_json = self._make_boto_call(action_result, 'create_bucket', Bucket=output_s3_bucket_name, CreateBucketConfiguration=location)

        return ret_val, output_s3_bucket_name

    def _get_s3_object(self, action_result, output_s3_bucket_name, output_s3_object_key, save_output_to_vault, file_name):

        self._create_s3_client(action_result)

        ret_val, resp_json = self._make_s3_boto_call(action_result, 'get_object', Bucket=output_s3_bucket_name, Key=output_s3_object_key)

        if (phantom.is_fail(ret_val)):
            return ret_val

        try:
            file_data = resp_json.pop('Body').read()
            # This conditional means 'get file' action has been called. Decodes the base64 string written by 'send command'
            if file_name:
                file_data = base64.b64decode(file_data)
        except:
            return action_result.set_status(phantom.APP_ERROR, "Could not retrieve object body from boto response")

        result_json = {}

        result_json['output'] = file_data

        if save_output_to_vault:
            if hasattr(file_data, 'decode'):
                file_data = file_data.decode('utf-8')
            if hasattr(Vault, 'get_vault_tmp_dir'):
                vault_path = Vault.get_vault_tmp_dir()
            else:
                vault_path = '/vault/tmp/'

            file_desc, file_path = tempfile.mkstemp(dir=vault_path)
            outfile = open(file_path, 'w')
            outfile.write(file_data)
            outfile.close()
            os.close(file_desc)

            try:
                # This conditional means 'get file' action has been called. This updates the correct filename that is written into the vault
                if file_name:
                    success, message, vault_id = ph_rules.vault_add(file_location=file_path, container=self.get_container_id(), file_name=file_name)
                    result_json['filename'] = file_name
                    # We do not need to return output for 'get file' action
                    result_json.pop('output', None)
                # This conditional means 'execute program' action has been called. This will name the file as either 'stdout' or 'stderr' into the vault
                else:
                    success, message, vault_id = ph_rules.vault_add(file_location=file_path, container=self.get_container_id(), file_name=os.path.basename(output_s3_object_key))
                    result_json['filename'] = os.path.basename(output_s3_object_key)
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, "Could not file to vault: {0}".format(e))

            if not success:
                return action_result.set_status(phantom.APP_ERROR, "Could not save file to vault: {0}".format(message))
            result_json['vault_id'] = vault_id
            action_result.set_summary({"created_vault_id": vault_id})

        result_json['s3_object_key'] = output_s3_object_key
        return ret_val, result_json

    def _handle_test_connectivity(self, param):

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        self.save_progress("Querying AWS to check credentials")

        if not self._create_client(action_result):
            return action_result.get_status()

        # make rest call
        ret_val, resp_json = self._make_boto_call(action_result, 'list_commands', MaxResults=1)

        if (phantom.is_fail(ret_val)):
            self.save_progress("Test Connectivity Failed.")
            return action_result.get_status()

        # Return success
        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_send_command(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))
        instance_id = param['instance_id']
        platform_type = param['platform_type']
        if platform_type == 'Windows':
            document_name = POWERSHELL_DOCUMENT
            document_hash = POWERSHELL_DOC_HASH
            object_path = 'awsrunPowerShellScript/0.awsrunPowerShellScript/stdout'
        else:
            document_name = LINUX_DOCUMENT
            document_hash = LINUX_DOC_HASH
            object_path = 'awsrunShellScript/0.awsrunShellScript/stdout'
        # If running get_file, 'cat' the file into an S3 bucket
        if self.get_action_identifier() == 'get_file':
            file_path = param['file_path'].replace('\\', '/')
            file_name = file_path.split('/')[-1]
            if platform_type == 'Windows':
                command = '[Convert]::ToBase64String([IO.File]::ReadAllBytes("{}"))'.format(file_path)
            else:
                command = 'cat ' + file_path + ' | base64'
            save_output_to_vault = True
        else:
            command = param['command']
            file_name = None
            save_output_to_vault = param.get('save_output_to_vault')

        output_s3_bucket_name = param.get('output_s3_bucket_name')
        working_directory = param.get('working_directory')
        timeout_seconds = param.get('timeout_seconds')
        comment = param.get('comment')

        if not output_s3_bucket_name:
            output_s3_bucket_name = self._default_s3_bucket

        # Create S3 bucket to store command output if it does not already exist
        if self._get_s3_bucket(action_result, output_s3_bucket_name) is False:
            ret_val, output_s3_bucket_name = self._create_s3_bucket(action_result, output_s3_bucket_name)
            if ret_val is False:
                return action_result.set_status(phantom.APP_ERROR, "Failed to create S3 bucket")

        args = {
            'InstanceIds': [instance_id],
            'DocumentName': document_name,
            'DocumentHash': document_hash,
            'DocumentHashType': 'Sha256',
            'OutputS3BucketName': output_s3_bucket_name,
            'Parameters': {
                'commands': [command]
            }
        }
        if working_directory:
            args['Parameters']['workingDirectory'] = [working_directory]
        if timeout_seconds:
            args['TimeoutSeconds'] = timeout_seconds
        if comment:
            args['Comment'] = comment

        if not self._create_client(action_result):
            return action_result.get_status()

        # Executes the shell program via SSM boto call
        ret_val, response = self._make_boto_call(action_result, 'send_command', **args)

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        result_json = {"Command": response['Command']}
        result_json['ResponseMetadata'] = response['ResponseMetadata']

        output_s3_object_key = response['Command']['CommandId'] + '/' + instance_id + '/' + object_path

        # Give time for command output to be written to S3 bucket
        time.sleep(10)

        try:
            ret_val, resp_json = self._get_s3_object(action_result, output_s3_bucket_name, output_s3_object_key, save_output_to_vault, file_name)
        except Exception:
            # Look for stderr file if stdout file was not found. If this is get_file action, then action fails with a no file found message.
            try:
                if self.get_action_identifier() == 'get_file':
                    return action_result.set_status(phantom.APP_ERROR, "{}: No such file found. Please check full file path (include filename)".format(file_path))
                output_s3_object_key = output_s3_object_key.replace('stdout', 'stderr')
                ret_val, resp_json = self._get_s3_object(action_result, output_s3_bucket_name, output_s3_object_key, save_output_to_vault, file_name)
            except Exception:
                return action_result.set_status(phantom.APP_ERROR, "Failed to get S3 object")

        result_json["File"] = resp_json

        # Add the response into the data section
        action_result.add_data(result_json)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        if self.get_action_identifier() == 'get_file':
            summary['status'] = "Successfully downloaded file into the vault"
        else:
            summary['status'] = "Successfully executed program"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_run_document(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        output_s3_bucket_name = param.get('output_s3_bucket_name')
        output_s3_key_prefix = param.get('output_s3_key_prefix')
        if output_s3_bucket_name:
            # Create S3 bucket to store command output if it does not already exist
            if self._get_s3_bucket(action_result, output_s3_bucket_name) is False:
                ret_val, output_s3_bucket_name = self._create_s3_bucket(action_result, output_s3_bucket_name)
                if ret_val is False:
                    return action_result.set_status(phantom.APP_ERROR, "Failed to create S3 bucket")

        if not self._create_client(action_result):
            return action_result.get_status()

        instance_id = param['instance_id']
        document_name = param['document_name']
        document_hash = param['document_hash']
        if phantom.is_sha1(document_hash):
            document_hash_type = 'Sha1'
        else:
            document_hash_type = 'Sha256'
        try:
            parameters = json.loads(param['parameters'])
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Invalid JSON for Parameters. Error: {0}".format(str(e))), None)
        working_directory = param.get('working_directory')
        timeout_seconds = param.get('timeout_seconds')
        comment = param.get('comment')

        args = {
            'InstanceIds': [instance_id],
            'DocumentName': document_name,
            'DocumentHash': document_hash,
            'DocumentHashType': document_hash_type,
            'Parameters': parameters
        }
        if working_directory:
            args['Parameters']['workingDirectory'] = [working_directory]
        if timeout_seconds:
            args['TimeoutSeconds'] = timeout_seconds
        if comment:
            args['Comment'] = comment
        if output_s3_bucket_name:
            args['OutputS3BucketName'] = output_s3_bucket_name
        if output_s3_key_prefix:
            args['OutputS3KeyPrefix'] = output_s3_key_prefix

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'send_command', **args)

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['status'] = "Successfully sent command"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_commands(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            return action_result.get_status()

        num_commands = 0

        while True:

            command_id = param.get('command_id')
            instance_id = param.get('instance_id')
            max_results = param.get('max_results')
            limit = None
            if max_results == 0:
                return action_result.set_status(phantom.APP_ERROR, "MaxResults parameter must be greater than 0")
            elif max_results is not None and max_results > 50:
                limit = max_results
                max_results = None
            next_token = param.get('next_token')

            args = {}
            if command_id:
                args['CommandId'] = command_id
            if instance_id:
                args['InstanceId'] = instance_id
            if max_results:
                args['MaxResults'] = max_results
            if next_token:
                args['NextToken'] = next_token

            # make rest call
            ret_val, response = self._make_boto_call(action_result, 'list_commands', **args)

            if (phantom.is_fail(ret_val)):
                return action_result.get_status()

            num_commands = num_commands + len(response['Commands'])

            # handles limitation of boto3 pagination results greater than 50
            if limit is not None:
                action_result.add_data(response)
                limit = limit - 50
                param['max_results'] = limit
                if response.get('NextToken'):
                    param['next_token'] = response.get('NextToken')
                    continue
                else:
                    # Add a dictionary that is made up of the most important values from data into the summary
                    summary = action_result.update_summary({})
                    summary['num_commands'] = num_commands
                    return action_result.set_status(phantom.APP_SUCCESS)

            # Add the response into the data section
            action_result.add_data(response)
            next_token = response.get('NextToken')

            if next_token and max_results is None:
                param['next_token'] = response['NextToken']
            else:
                # Add a dictionary that is made up of the most important values from data into the summary
                summary = action_result.update_summary({})
                summary['num_commands'] = num_commands
                return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_documents(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            return action_result.get_status()

        num_documents = 0

        while True:

            name = param.get('name')
            owner = param.get('owner')
            platform_type = param.get('platform_type')
            document_type = param.get('document_type')
            max_results = param.get('max_results')
            # This flag is to handle the special case where max_results is a number greater than 50
            flag = False
            if max_results == 0:
                return action_result.set_status(phantom.APP_ERROR, "MaxResults parameter must be greater than 0")
            elif max_results is not None and max_results > 50:
                limit = max_results
                max_results = None
                flag = True
            next_token = param.get('next_token')

            args = {}
            if name or owner or platform_type or document_type:
                args['DocumentFilterList'] = []

            if name:
                name_obj = {'key': 'Name', 'value': name}
                args['DocumentFilterList'].append(name_obj)
            if owner:
                owner_obj = {'key': 'Owner', 'value': owner}
                args['DocumentFilterList'].append(owner_obj)
            if platform_type:
                platform_obj = {'key': 'PlatformTypes', 'value': platform_type}
                args['DocumentFilterList'].append(platform_obj)
            if document_type:
                document_obj = {'key': 'DocumentType', 'value': document_type}
                args['DocumentFilterList'].append(document_obj)
            if max_results:
                args['MaxResults'] = max_results
            if next_token:
                args['NextToken'] = next_token

            # make rest call
            ret_val, response = self._make_boto_call(action_result, 'list_documents', **args)

            if (phantom.is_fail(ret_val)):
                return action_result.get_status()

            next_token = response.get('NextToken')

            # boto3 returning incorrect pagination results. This logic corrects the amount of results added
            if max_results is not None or flag:
                if flag:
                    upper_bound = limit - num_documents
                else:
                    upper_bound = max_results - num_documents
                if upper_bound > len(response['DocumentIdentifiers']):
                    for document in response['DocumentIdentifiers']:
                        action_result.add_data(document)
                    num_documents = num_documents + len(response['DocumentIdentifiers'])
                else:
                    for document in response['DocumentIdentifiers'][0:upper_bound]:
                        action_result.add_data(document)
                    num_documents = num_documents + len(response['DocumentIdentifiers'][0:upper_bound])
            else:
                for document in response['DocumentIdentifiers']:
                    action_result.add_data(document)
                num_documents = num_documents + len(response['DocumentIdentifiers'])

            if next_token and max_results is None:
                param['next_token'] = response['NextToken']
            elif max_results is not None and num_documents < max_results and next_token:
                param['next_token'] = response['NextToken']
            else:
                # Add a dictionary that is made up of the most important values from data into the summary
                summary = action_result.update_summary({})
                summary['num_documents'] = num_documents
                return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_parameter(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            return action_result.get_status()

        name = param['name']
        with_decryption = param.get('with_decryption', False)

        args = {
            'Name': name,
            'WithDecryption': with_decryption
        }

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'get_parameter', **args)

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['status'] = "Successfully retrieved parameter"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_add_parameter(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            return action_result.get_status()

        name = param['name']
        description = param.get('description')
        value = param['value']
        type = param['type']
        key_id = param.get('key_id')
        overwrite = param['overwrite']
        allowed_pattern = param.get('allowed_pattern')

        args = {
            'Name': name,
            'Value': value,
            'Type': type,
            'Overwrite': overwrite
        }

        if description:
            args['Description'] = description
        if key_id:
            args['KeyId'] = key_id
        if allowed_pattern:
            args['AllowedPattern'] = allowed_pattern

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'put_parameter', **args)

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['status'] = "Successfully added parameter"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_describe_instance(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            return action_result.get_status()

        instance_id = param['instance_id']
        instance_information_filter_list = [{'key': 'InstanceIds', 'valueSet': [instance_id]}]

        args = {
            'InstanceInformationFilterList': instance_information_filter_list
        }

        # make rest call
        ret_val, response = self._make_boto_call(action_result, 'describe_instance_information', **args)

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        if len(response['InstanceInformationList']) == 0:
            return action_result.set_status(phantom.APP_ERROR, "No SSM instance found. Please check if instance is assigned to a System Manager IAM role.")

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['status'] = "Successfully retrieved instance information"

        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)

        elif action_id == 'list_commands':
            ret_val = self._handle_list_commands(param)

        elif action_id == 'list_documents':
            ret_val = self._handle_list_documents(param)

        elif action_id == 'execute_program':
            ret_val = self._handle_send_command(param)

        elif action_id == 'get_file':
            ret_val = self._handle_send_command(param)

        elif action_id == 'run_document':
            ret_val = self._handle_run_document(param)

        elif action_id == 'get_parameter':
            ret_val = self._handle_get_parameter(param)

        elif action_id == 'add_parameter':
            ret_val = self._handle_add_parameter(param)

        elif action_id == 'describe_instance':
            ret_val = self._handle_describe_instance(param)

        return ret_val

    def initialize(self):

        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # Fetching the Python major version
        try:
            self._python_version = int(sys.version_info[0])
        except:
            return self.set_status(phantom.APP_ERROR, "Error occurred while getting the Phantom server's Python major version.")

        # get the asset config
        config = self.get_config()

        if SSM_JSON_ACCESS_KEY in config:
            self._access_key = config.get(SSM_JSON_ACCESS_KEY)
        if SSM_JSON_SECRET_KEY in config:
            self._secret_key = config.get(SSM_JSON_SECRET_KEY)
        if SSM_JSON_DEFAULT_S3_BUCKET in config:
            self._default_s3_bucket = config.get(SSM_JSON_DEFAULT_S3_BUCKET)

        self._region = SSM_REGION_DICT.get(config[SSM_JSON_REGION])

        self._proxy = {}
        env_vars = config.get('_reserved_environment_variables', {})
        if 'HTTP_PROXY' in env_vars:
            self._proxy['http'] = env_vars['HTTP_PROXY']['value']
        if 'HTTPS_PROXY' in env_vars:
            self._proxy['https'] = env_vars['HTTPS_PROXY']['value']

        return phantom.APP_SUCCESS

    def finalize(self):

        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == '__main__':

    import pudb
    import argparse

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if (username is not None and password is None):

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if (username and password):
        login_url = BaseConnector._get_phantom_base_url() + "login"
        try:
            print("Accessing the Login page")
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print("Unable to get session id from the platform. Error: {}".format(str(e)))
            exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = AwsSystemsManagerConnector()
        connector.print_progress_message = True

        if (session_id is not None):
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    exit(0)
