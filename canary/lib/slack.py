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
import json
import os
import inspect
from urllib.request import Request, urlopen, URLError, HTTPError
from urllib.parse import urlencode


class Slack(object):
    def __init__(self, logger, **kwargs):
        self.logger = logger
        if kwargs is not None:
            if kwargs.get('slack_channel') is None:
                logger.debug(f"Could not find a supplied slack channel to send to")
                self.slack_channel = None
            elif kwargs.get('slack_url') is None:
                logger.debug(f"Could not find a supplied slack workspace URL to send to")
                self.slack_url = None
            else:
                self.slack_channel = kwargs.get('slack_channel')
                self.slack_url = kwargs.get('slack_url')
                logger.info(f"Sending messages to slack {self.slack_url}/{self.slack_channel}")
        else:
            logger.debug("Did not recieve any kwargs to configure slack class")
            self.slack_url = None
            self.slack_channel = None

    def error_message(self, stack_trace, e):
        message = {'FILE': __file__.split('/')[-1], 'CLASS': self.__class__.__name__,
                'METHOD': stack_trace, 'EXCEPTION': str(e)}
        return message
        
    def slack_send_message(self, message):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            json.dumps(message)
            slack_message = {
                'channel': self.slack_channel,
                'text': message
            }
            self.logger.info(str(slack_message))
            req = Request(self.slack_url, json.dumps(slack_message))
            response = urlopen(req)
            self.logger.info(f"recieved response posting to slack: {response}")
        except HTTPError as e:
            self.logger.error(f"Request failed: {e.code} {e.reason}")
            raise
        except URLError as e:
            self.logger.error(f"Server connection failed: {e.reason}")
            raise
        except Exception as e:
            self.logger.error(self.error_message(method, e))
            raise