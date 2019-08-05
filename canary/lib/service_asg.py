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

#sasg_client = boto3.client('application-autoscaling', region_name="us-west-2")

class SASG(object):
    def __init__(self, logger, **kwargs):
        self.logger = logger
        if kwargs is not None:
            if kwargs.get('credentials') is None:
                logger.debug("Setting up {} BOTO3 Client with default credentials".format(self.__class__.__name__))
                self.sasg_client = boto3.client('application-autoscaling', region_name='us-west-2')
            elif kwargs.get('region') is not None:
                logger.debug("Setting up {} BOTO3 Client with default credentials in region {}".format(self.__class__.__name__, kwargs.get('region')))
                self.sasg_client = boto3.client('application-autoscaling', region_name=kwargs.get('region'))
            else:
                logger.debug("Setting up {} BOTO3 Client with ASSUMED ROLE credentials".format(self.__class__.__name__))
                cred = kwargs.get('credentials')
                self.sasg_client = boto3.client('application-autoscaling',
                                               aws_access_key_id=cred.get('AccessKeyId'),
                                               aws_secret_access_key=cred.get('SecretAccessKey'),
                                               aws_session_token=cred.get('SessionToken')
                                               )
        else:
            logger.debug("Setting up {} BOTO3 Client with default credentials".format(self.__class__.__name__))
            self.sasg_client = boto3.client('application-autoscaling')
    
    def error_message(self, stack_trace, e):
        message = {'FILE': __file__.split('/')[-1], 'CLASS': self.__class__.__name__,
                'METHOD': stack_trace, 'EXCEPTION': str(e)}
        return message

    def deregister_scalable_target_ecs(self, cluster, service):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.sasg_client.deregister_scalable_target(
                ServiceNamespace='ecs',
                ResourceId='service/{}/{}'.format(cluster, service),
                ScalableDimension='ecs:service:DesiredCount'
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def deregister_scalable_target_spot(self, ResourceId):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.sasg_client.deregister_scalable_target(
                ServiceNamespace='ec2',
                ResourceId='spot-fleet-request/{}'.format(ResourceId),
                ScalableDimension='ec2:spot-fleet-request:TargetCapacity'
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def register_scalable_target(self, ServiceNamespace, ResourceId, ScalableDimension, RoleARN, MinCapacity, MaxCapacity):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.sasg_client.register_scalable_target(
                ServiceNamespace=ServiceNamespace,
                ResourceId=ResourceId,
                ScalableDimension=ScalableDimension,
                RoleARN=RoleARN,
                MinCapacity=MinCapacity,
                MaxCapacity=MaxCapacity
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise
    
    def describe_scaling_policies(self, ServiceNamespace, ResourceIds):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.sasg_client.describe_scaling_policies(
                    ServiceNamespace=ServiceNamespace,
                    ResourceId=ResourceIds
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def describe_scalable_targets(self, ServiceNamespace, ResourceIds):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.sasg_client.describe_scalable_targets(
                    ServiceNamespace=ServiceNamespace,
                    ResourceIds=[
                        ResourceIds
                    ]
            )
            return response
        except Exception as e:
            self.logger.info(self.error_message(method, e))
            raise

    def put_scaling_policy_ts(self, **kwargs):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response =  self.sasg_client.put_scaling_policy(
            PolicyName=kwargs['PolicyName'],
            ServiceNamespace=kwargs['ServiceNamespace'],
            ResourceId=kwargs['ResourceId'],
            ScalableDimension=kwargs['ScalableDimension'],
            PolicyType=kwargs['PolicyType'],
            TargetTrackingScalingPolicyConfiguration={
                'TargetValue': kwargs['TargetValue'],
                'PredefinedMetricSpecification': {
                    'PredefinedMetricType': kwargs['PredefinedMetricType']
                },
                'ScaleOutCooldown': kwargs['ScaleOutCooldown'],
                'ScaleInCooldown': kwargs['ScaleInCooldown'],
            }
        )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def put_scaling_policy_ss(self, **kwargs):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response =  self.sasg_client.put_scaling_policy(
                PolicyName=kwargs['PolicyName'],
                ServiceNamespace=kwargs['ServiceNamespace'],
                ResourceId=kwargs['ResourceId'],
                ScalableDimension=kwargs['ScalableDimension'],
                PolicyType=kwargs['PolicyType'],
                StepScalingPolicyConfiguration={
                    'AdjustmentType': kwargs['AdjustmentType'],
                    #'MinAdjustmentMagnitude': kwargs['MinAdjustmentMagnitude'],
                    'Cooldown': int(kwargs['Cooldown']),
                    #'MetricAggregationType': kwargs['MetricAggregationType'],
                    'StepAdjustments': [
                        {
                            kwargs['MetricType']: kwargs['MetricValue'],
                            'ScalingAdjustment': int(kwargs['ScalingAdjustment'])
                        }
                    ]
                }
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise