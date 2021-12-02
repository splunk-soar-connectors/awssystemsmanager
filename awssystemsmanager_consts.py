# File: awssystemsmanager_consts.py
#
# Copyright (c) 2019-2021 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
#
# Define your constants here
SSM_JSON_ACCESS_KEY = "access_key"
SSM_JSON_SECRET_KEY = "secret_key"
SSM_JSON_REGION = "region"
SSM_JSON_DEFAULT_S3_BUCKET = "default_s3_bucket"
SSM_JSON_BAD_ASSET_CONFIG_MSG = "Please provide access keys or select assume role check box in asset configuration"

SSM_REGION_DICT = {
        "US East (N. Virginia)": "us-east-1",
        "US East (Ohio)": "us-east-2",
        "US West (N. California)": "us-west-1",
        "US West (Oregon)": "us-west-2",
        "Asia Pacific (Hong Kong)": "ap-east-1",
        "Asia Pacific (Mumbai)": "ap-south-1",
        "Asia Pacific (Seoul)": "ap-northeast-2",
        "Asia Pacific (Singapore)": "ap-southeast-1",
        "Asia Pacific (Sydney)": "ap-southeast-2",
        "Asia Pacific (Tokyo)": "ap-northeast-1",
        "Canada (Central)": "ca-central-1",
        "China (Beijing)": "cn-north-1",
        "China (Ningxia)": "cn-northwest-1",
        "EU (Frankfurt)": "eu-central-1",
        "EU (Ireland)": "eu-west-1",
        "EU (London)": "eu-west-2",
        "EU (Paris)": "	eu-west-3",
        "EU (Stockholm)": "eu-north-1",
        "South America (Sao Paulo)": "sa-east-1",
        "AWS GovCloud (US-East)": "us-gov-east-1",
        "AWS GovCloud (US)": "us-gov-west-1"
    }

POWERSHELL_DOCUMENT = 'AWS-RunPowerShellScript'
POWERSHELL_DOC_HASH = '2142e42a19e0955cc09e43600bf2e633df1917b69d2be9693737dfd62e0fdf61'
LINUX_DOCUMENT = 'AWS-RunShellScript'
LINUX_DOC_HASH = '99749de5e62f71e5ebe9a55c2321e2c394796afe7208cff048696541e6f6771e'
