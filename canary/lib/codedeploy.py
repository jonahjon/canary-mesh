#!/bin/python
######################################################################################################################
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

#cd_client = boto3.client('codedeploy', region_name='us-west-2')
class Codedeploy(object):
    def __init__(self, logger, **kwargs):
        self.logger = logger
        if kwargs is not None:
            if kwargs.get('credentials') is None:
                logger.debug("Setting up {} BOTO3 Client with default credentials".format(self.__class__.__name__))
                self.cd_client = boto3.client('codedeploy', region_name='us-west-2')
            elif kwargs.get('region') is not None:
                logger.debug("Setting up {} BOTO3 Client with default credentials in region {}".format(self.__class__.__name__, kwargs.get('region')))
                self.cd_client = boto3.client('codedeploy', region_name=kwargs.get('region'))
            else:
                logger.debug("Setting up {} BOTO3 Client with ASSUMED ROLE credentials".format(self.__class__.__name__))
                cred = kwargs.get('credentials')
                self.cd_client = boto3.client('codedeploy',
                                               aws_access_key_id=cred.get('AccessKeyId'),
                                               aws_secret_access_key=cred.get('SecretAccessKey'),
                                               aws_session_token=cred.get('SessionToken')
                                               )
        else:
            logger.debug("Setting up {} BOTO3 Client with default credentials".format(self.__class__.__name__))
            self.cd_client = boto3.client('codedeploy')

    def error_message(self, stack_trace, e):
        message = {'FILE': __file__.split('/')[-1], 'CLASS': self.__class__.__name__,
                'METHOD': stack_trace, 'EXCEPTION': str(e)}
        return message

    def success(self, deploymentid, lifecycleEventHookExecutionId):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.cd_client.put_lifecycle_event_hook_execution_status(
                deploymentId=deploymentid,
                lifecycleEventHookExecutionId=lifecycleEventHookExecutionId,
                status='Succeeded'
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def fail(self, deploymentid, lifecycleEventHookExecutionId):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.cd_client.put_lifecycle_event_hook_execution_status(
                deploymentId=deploymentid,
                lifecycleEventHookExecutionId=lifecycleEventHookExecutionId,
                status='Failed'
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def pending(self, deploymentid, lifecycleEventHookExecutionId):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.cd_client.put_lifecycle_event_hook_execution_status(
                deploymentId=deploymentid,
                lifecycleEventHookExecutionId=lifecycleEventHookExecutionId,
                status='Pending'
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def get_deployment(self, deployid):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.cd_client.get_deployment(
                deploymentId=deployid
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def list_deployments(self, includeOnlyStatuses, deploymentGroupName):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.cd_client.list_deployments(
            applicationName=deploymentGroupName,
            includeOnlyStatuses=[includeOnlyStatuses],
            deploymentGroupName=deploymentGroupName,
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise
    
    def hard_stop_deployment(self, deployid):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.cd_client.stop_deployment(
                deploymentId=deployid,
                autoRollbackEnabled=True
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise