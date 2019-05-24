# File: awssystemsmanager_consts.py
# Copyright (c) 2019 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.
# Define your constants here

SSM_JSON_ACCESS_KEY = "access_key"
SSM_JSON_SECRET_KEY = "secret_key"
SSM_JSON_REGION = "region"

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
