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
from .validators import validate_input, type_check

#pipe_client = boto3.client('appmesh', region_name="us-west-2")
class AppMesh(object):
    def __init__(self, logger, **kwargs):
        self.logger = logger
        self.mesh_name = kwargs.get('mesh', 'sample-mesh')
        if kwargs is not None:
            if kwargs.get('credentials') is None:
                logger.debug("Setting up {} BOTO3 Client with default credentials".format(self.__class__.__name__))
                self.mesh_client = boto3.client('appmesh', region_name='us-west-2')
            elif kwargs.get('region') is not None:
                logger.debug("Setting up {} BOTO3 Client with default credentials in region {}".format(self.__class__.__name__, kwargs.get('region')))
                self.mesh_client = boto3.client('appmesh', region_name=kwargs.get('region'))
            else:
                logger.debug("Setting up {} BOTO3 Client with ASSUMED ROLE credentials".format(self.__class__.__name__))
                cred = kwargs.get('credentials')
                self.mesh_client = boto3.client('appmesh',
                                               aws_access_key_id=cred.get('AccessKeyId'),
                                               aws_secret_access_key=cred.get('SecretAccessKey'),
                                               aws_session_token=cred.get('SessionToken')
                                               )
        else:
            logger.debug("Setting up {} BOTO3 Client with default credentials".format(self.__class__.__name__))
            self.mesh_client = boto3.client('appmesh')
        

    def error_message(self, stack_trace, e):
        message = {'FILE': __file__.split('/')[-1], 'CLASS': self.__class__.__name__,
                'METHOD': stack_trace, 'EXCEPTION': str(e)}
        return message

    def check_mesh_exists(self):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            mesh_info = self.describe_mesh(mesh=self.mesh_name)
            if mesh_info['mesh']['meshName'] == self.mesh_name:
                self.logger.info(f"Found existing service mesh {self.mesh_name}")
                self.mesh = self.mesh_name
                return True
            else:
                self.logger.info(f"Did not findd existing service mesh, creating one: {self.mesh_name}")
                meshinfo = self.create_mesh(mesh=self.mesh_name)
                self.mesh = meshinfo['mesh']['meshName']
                return True
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    def create_mesh(self, mesh):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response  = self.mesh_client.create_mesh(meshName=mesh)
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise
    
    def describe_mesh(self, mesh):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            response = self.mesh_client.describe_mesh(
                meshName = mesh
            )
            self.logger.info(response)
            return response
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise

    # ### TODO
    # def check_virtual_node_exists(self, virtualRouterName):
    #     method = inspect.stack()[0][3]
    #     self.logger.info('Executing function {}'.format(method))
    #     try:
    #         self.mesh_client.create_virtual_node()
    #         return
    #     except Exception as e:
    #         self.logger.exception(self.error_message(method, e))
    #         raise

    # ### TODO
    # def create_virtual_node(self, virtualRouterName):
    #     method = inspect.stack()[0][3]
    #     self.logger.info('Executing function {}'.format(method))
    #     try:
    #         self.mesh_client.create_virtual_node(
    #             meshName=self.mesh,

    #         )
    #     except Exception as e:
    #         self.logger.exception(self.error_message(method, e))
    #         raise

    # def describe_virtual_node(self, virtualNodeName):
    #     method = inspect.stack()[0][3]
    #     self.logger.info('Executing function {}'.format(method))
    #     try:
    #         response = self.mesh_client.describe_virtual_node(
    #             meshName=self.mesh,
    #             virtualNodeName=virtualNodeName
    #         )
    #         return response
    #     except Exception as e:
    #         self.logger.exception(self.error_message(method, e))
    #         raise

    #  ### TODO
    # def check_virtual_router_exists(self, virtualRouterName):
    #     method = inspect.stack()[0][3]
    #     self.logger.info('Executing function {}'.format(method))
    #     try:
    #         self.mesh_client.describe_virtual_router()
    #         return
    #     except Exception as e:
    #         self.logger.exception(self.error_message(method, e))
    #         raise

    # ### TODO
    # def create_virtual_router(self, virtualRouterName):
    #     method = inspect.stack()[0][3]
    #     self.logger.info('Executing function {}'.format(method))
    #     try:
    #         spec = self.create_route_spec(

    #         )
    #         self.mesh_client.create_virtualrouter()
    #     except Exception as e:
    #         self.logger.exception(self.error_message(method, e))
    #         raise

    # ### TODO
    # def describe_virtual_router(self, virtualRouterName):
    #     method = inspect.stack()[0][3]
    #     self.logger.info('Executing function {}'.format(method))
    #     try:
    #         self.mesh_client.describe_virtualrouter()
    #     except Exception as e:
    #         self.logger.exception(self.error_message(method, e))
    #         raise

    # def describe_route(self, meshName, routeName, virtualRouterName):
    #     method = inspect.stack()[0][3]
    #     self.logger.info('Executing function {}'.format(method))
    #     try:
    #         response = self.mesh_client.describe_route(
    #             meshName=meshName,
    #             routeName=routeName,
    #             virtualRouterName=virtualRouterName
    #         )
    #         return response
    #     except Exception as e:
    #         self.logger.exception(self.error_message(method, e))
    #         raise
            
    # def update_route(self, **kwargs):
    #     method = inspect.stack()[0][3]
    #     self.logger.info('Executing function {}'.format(method))
    #     try:
    #         response = self.mesh_client.update_route(
    #             meshName=kwargs['meshName'],
    #             spec=kwargs['spec'],
    #             virtualRouterName=kwargs['virtualRouterName']
    #         )
    #         return response
    #     except Exception as e:
    #         self.logger.exception(self.error_message(method, e))
    #         raise
    

    @type_check
    def create_route_spec(self, protocol: str, virtual_node: str, weight: int, **kwargs: dict):
        method = inspect.stack()[0][3]
        self.logger.info('Executing function {}'.format(method))
        try:
            route = {}
            route[f"{protocol}Route"] = {
                'action':{
                    'weightedTargets':[
                        {
                            'virtualNode':f"{virtual_node}",
                            'weight': f"{weight}"
                        }
                    ]
                },
                'match':{
                    'prefix':kwargs.get('prefix', '/')
                }
            }
            return route
        except Exception as e:
            self.logger.exception(self.error_message(method, e))
            raise
        