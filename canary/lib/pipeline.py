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

#pipe_client = boto3.client('codepipeline', region_name="us-west-2")
class Pipeline(object):
    def __init__(self, logger, **kwargs):
        self.logger = logger
        if kwargs is not None:
            if kwargs.get('credentials') is None:
                logger.debug("Setting up {} BOTO3 Client with default credentials".format(self.__class__.__name__))
                self.pipe_client = boto3.client('codepipeline', region_name='us-west-2')
            elif kwargs.get('region') is not None:
                logger.debug("Setting up {} BOTO3 Client with default credentials in region {}".format(self.__class__.__name__, kwargs.get('region')))
                self.pipe_client = boto3.client('codepipeline', region_name=kwargs.get('region'))
            else:
                logger.debug("Setting up {} BOTO3 Client with ASSUMED ROLE credentials".format(self.__class__.__name__))
                cred = kwargs.get('credentials')
                self.pipe_client = boto3.client('codepipeline',
                                               aws_access_key_id=cred.get('AccessKeyId'),
                                               aws_secret_access_key=cred.get('SecretAccessKey'),
                                               aws_session_token=cred.get('SessionToken')
                                               )
        else:
            logger.debug("Setting up {} BOTO3 Client with default credentials".format(self.__class__.__name__))
            self.pipe_client = boto3.client('codepipeline')

    def error_message(self, stack_trace, e):
        message = {'FILE': __file__.split('/')[-1], 'CLASS': self.__class__.__name__,
                'METHOD': stack_trace, 'EXCEPTION': str(e)}
        return message
        
    def get_pipeline_state(self, name):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.pipe_client.get_pipeline_state(
                name=name
            )
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise
            
    def put_job_success(self, job_id):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            self.logger.info("Signaling completion to pipeline for job: {}".format(job_id))
            self.pipe_client.put_job_success_result(jobId=job_id)
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def put_job_failure(self, job_id, message):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            if len(message) > 265:
                message = message[0:211] + '... For full details see CloudWatch logs.'
            self.logger.info("Signaling failure to pipeline for job: {} errorMessage: {}".format(job_id, message))

            self.pipe_client.put_job_failure_result(
                jobId=job_id,
                failureDetails={'message': message, 'type': 'JobFailed'}
            )
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise