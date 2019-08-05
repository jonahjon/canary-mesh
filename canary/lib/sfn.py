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

#sfn_client = boto3.client('stepfunctions', region_name="us-west-2")
class StepFunction(object):
    def __init__(self, logger, **kwargs):
        self.logger = logger
        if kwargs is not None:
            if kwargs.get('credentials') is None:
                logger.debug("Setting up {} BOTO3 Client with default credentials".format(self.__class__.__name__))
                self.sfn_client = boto3.client('stepfunctions', region_name='us-west-2')
            elif kwargs.get('region') is not None:
                logger.debug("Setting up {} BOTO3 Client with default credentials in region {}".format(self.__class__.__name__, kwargs.get('region')))
                self.sfn_client = boto3.client('stepfunctions', region_name=kwargs.get('region'))
            else:
                logger.debug("Setting up {} BOTO3 Client with ASSUMED ROLE credentials".format(self.__class__.__name__))
                cred = kwargs.get('credentials')
                self.sfn_client = boto3.client('stepfunctions',
                                               aws_access_key_id=cred.get('AccessKeyId'),
                                               aws_secret_access_key=cred.get('SecretAccessKey'),
                                               aws_session_token=cred.get('SessionToken')
                                               )
        else:
            logger.debug("Setting up {} BOTO3 Client with default credentials".format(self.__class__.__name__))
            self.sfn_client = boto3.client('stepfunctions')

    def error_message(self, stack_trace, e):
        message = {'FILE': __file__.split('/')[-1], 'CLASS': self.__class__.__name__,
                'METHOD': stack_trace, 'EXCEPTION': str(e)}
        return message
        
    def start_execution(self, stateMachineArn, name, input):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.sfn_client.start_execution(
                stateMachineArn=stateMachineArn,
                name=name,
                input=input
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise