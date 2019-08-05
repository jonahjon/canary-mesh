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
#asg_client = boto3.client('autoscaling', region_name="us-west-2")

class ASG(object):
    def __init__(self, logger, **kwargs):
        self.logger = logger
        if kwargs is not None:
            if kwargs.get('credentials') is None:
                logger.debug("Setting up {} BOTO3 Client with default credentials".format(self.__class__.__name__))
                self.asg_client = boto3.client('autoscaling', region_name='us-west-2')
            elif kwargs.get('region') is not None:
                logger.debug("Setting up {} BOTO3 Client with default credentials in region {}".format(self.__class__.__name__, kwargs.get('region')))
                self.asg_client = boto3.client('autoscaling', region_name=kwargs.get('region'))
            else:
                logger.debug("Setting up {} BOTO3 Client with ASSUMED ROLE credentials".format(self.__class__.__name__))
                cred = kwargs.get('credentials')
                self.asg_client = boto3.client('autoscaling',
                                               aws_access_key_id=cred.get('AccessKeyId'),
                                               aws_secret_access_key=cred.get('SecretAccessKey'),
                                               aws_session_token=cred.get('SessionToken')
                                               )
        else:
            logger.debug("Setting up {} BOTO3 Client with default credentials".format(self.__class__.__name__))
            self.asg_client = boto3.client('autoscaling')

    def error_message(self, stack_trace, e):
        message = {'FILE': __file__.split('/')[-1], 'CLASS': self.__class__.__name__,
                'METHOD': stack_trace, 'EXCEPTION': str(e)}
        return message
        
    def suspend_asg_except_launch(self, AutoScalingGroupName):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.asg_client.suspend_processes(
                AutoScalingGroupName=AutoScalingGroupName,
                    # Here we have to specify pausing all actions besides Launching
                    # This allows us to pause scaling actions, and manually scale to double the size to handle B/G
                    ScalingProcesses=[
                        'Terminate',
                        'HealthCheck',
                        'ReplaceUnhealthy',
                        'AZRebalance',
                        'AlarmNotification',
                        'ScheduledActions',
                        'AddToLoadBalancer'
                    ]
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def resume_processes(self, AutoScalingGroupName):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.asg_client.resume_processes(
                AutoScalingGroupName=AutoScalingGroupName,
                    # Here we have to specify pausing all actions besides Launching
                    # This allows us to pause scaling actions, and manually scale to double the size to handle B/G
                    ScalingProcesses=[
                        'Terminate',
                        'HealthCheck',
                        'ReplaceUnhealthy',
                        'AZRebalance',
                        'AlarmNotification',
                        'ScheduledActions',
                        'AddToLoadBalancer'
                    ]
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def describe_auto_scaling_group_size(self, AutoScalingGroupName):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.asg_client.describe_auto_scaling_groups(
                AutoScalingGroupNames=[
                    AutoScalingGroupName,
                ]
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise


    def update_asg(self, AutoScalingGroupName, MinSize, MaxSize, DesiredCapacity):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.asg_client.update_auto_scaling_group(
                AutoScalingGroupName=AutoScalingGroupName,
                MinSize=MinSize,
                MaxSize=MaxSize,
                DesiredCapacity=DesiredCapacity
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise
    
    def get_paginator(self, name):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            paginator = self.asg_client.get_paginator(name)
            return paginator
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise


    def get_name_by_tag(self, TagKey, TagValue):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            paginator = self.asg_client.get_paginator('describe_auto_scaling_groups')
            page_iterator = paginator.paginate(
                PaginationConfig={'PageSize': 100}
            )
            filtered_asgs = page_iterator.search(
                'AutoScalingGroups[] | [?contains(Tags[?Key==`{}`].Value, `{}`)]'.format(
                    TagKey, TagValue)
            )
            for asg in filtered_asgs:
                self.logger.info("Found Groups with matching tags {}".format(asg['AutoScalingGroupName']))
                return asg['AutoScalingGroupName']
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise
