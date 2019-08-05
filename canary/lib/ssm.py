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
#ssm_client = boto3.client('ssm', region_name="us-west-2")

class SSM(object):
    def __init__(self, logger, **kwargs):
        self.logger = logger
        if kwargs is not None:
            if kwargs.get('credentials') is None:
                logger.debug("Setting up {} BOTO3 Client with default credentials".format(self.__class__.__name__))
                self.ssm_client = boto3.client('ssm')
            elif kwargs.get('region') is not None:
                logger.debug("Setting up {} BOTO3 Client with default credentials in region {}".format(self.__class__.__name__, kwargs.get('region')))
                self.ssm_client = boto3.client('ssm', region_name=kwargs.get('region'))
            else:
                logger.debug("Setting up {} BOTO3 Client with ASSUMED ROLE credentials".format(self.__class__.__name__))
                cred = kwargs.get('credentials')
                self.ssm_client = boto3.client('ssm',
                                               aws_access_key_id=cred.get('AccessKeyId'),
                                               aws_secret_access_key=cred.get('SecretAccessKey'),
                                               aws_session_token=cred.get('SessionToken')
                                               )
        else:
            logger.debug("Setting up {} BOTO3 Client with default credentials".format(self.__class__.__name__))
            self.ssm_client = boto3.client('ssm')

    def error_message(self, stack_trace, e):
        message = {'FILE': __file__.split('/')[-1], 'CLASS': self.__class__.__name__,
                'METHOD': stack_trace, 'EXCEPTION': str(e)}
        return message

    def put_parameter(self, name, value, description="This is used for Codedeploy Hooks", type='String', overwrite=True):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.ssm_client.put_parameter(
                Name=name,
                Value=value,
                Description=description,
                Type=type,
                Overwrite=overwrite,
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def get_parameter(self, name):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.ssm_client.get_parameter(
                Name=name,
                WithDecryption=True
            )
            return response.get('Parameter', {}).get('Value')
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def delete_parameter(self, name):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.ssm_client.delete_parameter(
                Name=name
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def get_parameters_by_path(self, path):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.ssm_client.get_parameters_by_path(
                Path=path if path.startswith('/') else '/'+path,
                Recursive=False,
                WithDecryption=True
            )
            params_list = response.get('Parameters', [])
            next_token = response.get('NextToken', None)

            while next_token is not None:
                response = self.ssm_client.get_parameters_by_path(
                    Path=path if path.startswith('/') else '/' + path,
                    Recursive=False,
                    WithDecryption=True,
                    NextToken=next_token
                )
                params_list.extend(response.get('Parameters', []))
                next_token = response.get('NextToken', None)
            return params_list
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def delete_parameters_by_path(self, name):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            params_list = self.ssm_client.get_parameters_by_path(name)
            if params_list:
                for param in params_list:
                    self.delete_parameter(param.get('Name'))
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def describe_parameters(self, parameter_name, begins_with=False):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.ssm_client.describe_parameters(
                ParameterFilters=[
                    {
                        'Key': 'Name',
                        'Option': 'BeginsWith' if begins_with else 'Equals',
                        'Values': [parameter_name]
                    }
                ]
            )
            parameters = response.get('Parameters', [])
            if parameters:
                return parameters[0]
            else:
                return None
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise