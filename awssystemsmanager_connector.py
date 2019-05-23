# File: awssystemsmanager_connector.py
# Copyright (c) 2019 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

# Usage of the consts file is recommended
from awssystemsmanager_consts import *
from boto3 import client
from datetime import datetime
from botocore.config import Config
import botocore.response as br
import botocore.paginate as bp
import requests
import json
# import base64


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
        self._proxy = None

    def _sanitize_data(self, cur_obj):

        try:
            json.dumps(cur_obj)
            return cur_obj
        except:
            pass

        if isinstance(cur_obj, dict):
            new_dict = {}
            for k, v in cur_obj.iteritems():
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
                exception_message = e.args[0].encode('utf-8').strip()
                return RetVal(action_result.set_status(phantom.APP_ERROR, 'boto3 call to SSM failed', exception_message), None)
        else:
            try:
                paginator = self._client.get_paginator(method)
                resp_json = paginator.paginate(**kwargs)
            except Exception as e:
                return RetVal(action_result.set_status(phantom.APP_ERROR, 'boto3 call to SSM failed', e), None)

        return phantom.APP_SUCCESS, self._sanitize_data(resp_json)

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

        if not self._create_client(action_result):
            return action_result.get_status()

        instance_ids = param['instance_ids'].replace(" ", "").split(",")
        platform_type = param['platform_type']
        if platform_type == 'Windows':
            document_name = POWERSHELL_DOCUMENT
            document_hash = POWERSHELL_DOC_HASH
        else:
            document_name = LINUX_DOCUMENT
            document_hash = LINUX_DOC_HASH
        commands = param['commands'].split(",")
        working_directory = param.get('working_directory')
        timeout_seconds = param.get('timeout_seconds')
        comment = param.get('comment')
        output_s3_bucket_name = param.get('output_s3_bucket_name')
        output_s3_key_prefix = param.get('output_s3_key_prefix')

        args = {
            'InstanceIds': instance_ids,
            'DocumentName': document_name,
            'DocumentHash': document_hash,
            'DocumentHashType': 'Sha256',
            'Parameters': {
                'commands': commands
            }
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
        summary['status'] = "Successfully executed commands"

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_run_document(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result):
            return action_result.get_status()

        instance_ids = param['instance_ids'].replace(" ", "").split(",")
        document_name = param['document_name']
        document_hash = param['document_hash']
        document_hash_type = param['document_hash_type']
        parameters = json.loads(param['parameters'])
        working_directory = param.get('working_directory')
        timeout_seconds = param.get('timeout_seconds')
        comment = param.get('comment')
        output_s3_bucket_name = param.get('output_s3_bucket_name')
        output_s3_key_prefix = param.get('output_s3_key_prefix')

        args = {
            'InstanceIds': instance_ids,
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
        summary['status'] = "Successfully executed document"

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
            if max_results == 0:
                return action_result.set_status(phantom.APP_ERROR, u"MaxResults parameter must be in valid range 1-50")
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

            # Add the response into the data section
            action_result.add_data(response)
            next_token = response.get('NextToken')
            num_commands = num_commands + len(response['Commands'])

            if next_token and max_results is None:
                param['next_token'] = response['NextToken']
            else:
                # Add a dictionary that is made up of the most important values from data into the summary
                summary = action_result.update_summary({})
                summary['num_commands'] = num_commands
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

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)

        elif action_id == 'list_commands':
            ret_val = self._handle_list_commands(param)

        elif action_id == 'execute_program':
            ret_val = self._handle_send_command(param)

        elif action_id == 'run_document':
            ret_val = self._handle_run_document(param)

        elif action_id == 'get_parameter':
            ret_val = self._handle_get_parameter(param)

        elif action_id == 'add_parameter':
            ret_val = self._handle_add_parameter(param)

        return ret_val

    def initialize(self):

        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()

        if SSM_JSON_ACCESS_KEY in config:
            self._access_key = config.get(SSM_JSON_ACCESS_KEY)
        if SSM_JSON_SECRET_KEY in config:
            self._secret_key = config.get(SSM_JSON_SECRET_KEY)

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
            print ("Accessing the Login page")
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print ("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print ("Unable to get session id from the platform. Error: " + str(e))
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
        print (json.dumps(json.loads(ret_val), indent=4))

    exit(0)
