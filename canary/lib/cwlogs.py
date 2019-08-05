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
import inspect
import time
from botocore.exceptions import ClientError, ParamValidationError



#log_client = boto3.client('logs', region_name="us-west-2")

class Logs(object):
    def __init__(self, **kwargs):
        if kwargs is not None:
            if kwargs.get('credentials') is None:
                print("Setting up {} BOTO3 Client with default credentials".format(self.__class__.__name__))
                self.log_client = boto3.client('logs', region_name='us-west-2')
            elif kwargs.get('region') is not None:
                print("Setting up {} BOTO3 Client with default credentials in region {}".format(self.__class__.__name__, kwargs.get('region')))
                self.log_client = boto3.client('logs', region_name=kwargs.get('region'))
            else:
                print("Setting up {} BOTO3 Client with ASSUMED ROLE credentials".format(self.__class__.__name__))
                cred = kwargs.get('credentials')
                self.log_client = boto3.client('logs',
                                               aws_access_key_id=cred.get('AccessKeyId'),
                                               aws_secret_access_key=cred.get('SecretAccessKey'),
                                               aws_session_token=cred.get('SessionToken')
                                               )
        else:
            print("Setting up {} BOTO3 Client with default credentials".format(self.__class__.__name__))
            self.log_client = boto3.client('logs')

    def error_message(self, stack_trace, e):
        message = {'FILE': __file__.split('/')[-1], 'CLASS': self.__class__.__name__,
                'METHOD': stack_trace, 'EXCEPTION': str(e)}
        return message

    def create_log_group(self, logGroupName):
        method = inspect.stack()[0][3]
        print(f"Executing function {method}")
        try:
            response = self.log_client.create_log_group(
                logGroupName=logGroupName
            )
            return response
        except self.log_client.exceptions.ResourceAlreadyExistsException:
            print(f"already have log group using..... {logGroupName}")
        except Exception as e:
            error = self.error_message(method, e)
            print(f"{error}")
            raise

    def create_log_stream(self, logGroupName, logStreamName):
        method = inspect.stack()[0][3]
        print(f"Executing function {method}")
        try:
            response = self.log_client.create_log_stream(
                logGroupName=logGroupName,
                logStreamName=logStreamName
            )
            return response
        except self.log_client.exceptions.ResourceAlreadyExistsException:
            print(f"already have log stream using .... {logStreamName}")
        except Exception as e:
            error = self.error_message(method, e)
            print(f"{error}")
            raise

    def describe_log_group(self, logGroupName):
        method = inspect.stack()[0][3]
        print(f"Executing function {method}")
        try:
            response = self.log_client.describe_log_groups(
                    logGroupNamePrefix=logGroupName
            )
            try:
                logGroup = response['logGroups'][0]['logGroupName']
                return logGroup
            except Exception as e:
                return None
        except Exception as e:
            error = self.error_message("describe_log_group", e)
            print(f"{error}")
            raise

    def describe_log_streams(self, logGroupName, logStreamName):
        method = inspect.stack()[0][3]
        print(f"Executing function {method}")
        try:
            response = self.log_client.describe_log_streams(
                logGroupName=logGroupName,
                logStreamNamePrefix=logStreamName
            )
            return response
        except Exception as e:
            error = self.error_message("describe_log_streams", e)
            print(f"{error}")
            raise

    def describe_log_stream_sequence_token(self, logGroupName, logStreamName):
        try:
            response = self.log_client.describe_log_streams(
                logGroupName=logGroupName,
                logStreamNamePrefix=logStreamName
            )
            try:
                uploadSequenceToken = response['logStreams'][0]['uploadSequenceToken']
                return uploadSequenceToken
            except Exception as e:
                return None
        except Exception as e:
            error = self.error_message("describe_log_stream_sequence_token", e)
            print(f"{error}")
            raise

    def put_log_events(self, logGroupName, logStreamName, logEvents, **kwargs):
        # Converts time in seconds to milliseconds for boto3
        timestamp = int(round(time.time() * 1000))
        try:
            uploadSequenceToken = self.describe_log_stream_sequence_token(logGroupName=logGroupName, logStreamName=logStreamName)
            if uploadSequenceToken is not None:
                response = self.log_client.put_log_events(logGroupName=logGroupName, logStreamName=logStreamName, sequenceToken=uploadSequenceToken,
                    logEvents=[
                        {
                            'timestamp': timestamp,
                            'message': logEvents
                        }
                    ]
                )
                return response
            elif kwargs['token_pass']:
                response = self.log_client.put_log_events(logGroupName=logGroupName, logStreamName=logStreamName,
                    logEvents=[
                        {
                            'timestamp': timestamp,
                            'message': logEvents
                        }
                    ]
                )
            else:
                pass
        except KeyError as e:
            return
        except self.log_client.exceptions.ResourceNotFoundException as e:
            return
        except Exception as e:
            error = self.error_message("put_logs", e)
            print(f"{error}")
            raise

