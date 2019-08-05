#!/bin/python
# ######################################################################################################################
#  Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                           #
#                                                                                                                    #
#  Licensed under the Amazon Software License (the "License"). You may not use this file except in compliance        #
#  with the License. A copy of the License is located at                                                             #
#                                                                                                                    #
#      http://aws.amazon.com/asl/                                                                                    #
#                                                                                                                    #
#  or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES #
#  OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions    #
#  and limitations under the License.                                                                                #
######################################################################################################################

import boto3
from base64 import b64decode
from datetime import datetime
import inspect
import json
import os

#s3_client = boto3.client('s3', region_name="us-west-2")

from datetime import datetime
import json

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


class S3(object):
    def __init__(self, logger, **kwargs):
        self.logger = logger
        if kwargs is not None:
            if kwargs.get('credentials') is None:
                logger.debug("Setting up {} BOTO3 Resource with default credentials".format(self.__class__.__name__))
                self.s3_client = boto3.resource('s3')
            elif kwargs.get('region') is not None:
                logger.debug("Setting up {} BOTO3 Resource with default credentials in region {}".format(self.__class__.__name__, kwargs.get('region')))
                self.s3_client = boto3.resource('s3', region_name=kwargs.get('region'))
            else:
                logger.debug("Setting up {} BOTO3 Resource with ASSUMED ROLE credentials".format(self.__class__.__name__))
                cred = kwargs.get('credentials')
                self.s3_client = boto3.resource('s3',
                                               aws_access_key_id=cred.get('AccessKeyId'),
                                               aws_secret_access_key=cred.get('SecretAccessKey'),
                                               aws_session_token=cred.get('SessionToken')
                                               )
        else:
            logger.debug("Setting up {} BOTO3 Resource with default credentials".format(self.__class__.__name__))
            self.s3_client = boto3.resource('s3')

    def error_message(self, stack_trace, e):
        message = {'FILE': __file__.split('/')[-1], 'CLASS': self.__class__.__name__,
                'METHOD': stack_trace, 'EXCEPTION': str(e)}
        return message
        
# from base64 import b64decode
# import json
# import boto3
# def lambda_handler(event, context):
#     s3 = boto3.resource('s3')
#     for rec in event['Records']:
#         data = json.loads(b64decode(rec['kinesis']['data']))
#         s3.Object('your-bucket', 'your-key').put(
#             Body=(bytes(json.dumps(data, indent=2).encode('UTF-8')))
#         )
    def upload_file(self, filename, dictionary, bucket_name):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            self.s3_client.Object(bucket_name, filename).put(Body=(json.dumps(dictionary, cls=DateTimeEncoder, indent=2)))
            return
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def download_file(self, filename, bucket_name):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            file_content = self.s3_client.Object(bucket_name, filename).get()['Body'].read().decode('UTF-8')
            json_content = json.loads(file_content)
            return json_content
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise