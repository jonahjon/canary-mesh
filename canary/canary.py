import boto3
import inspect
import os
from lib.logger import Logger
from lib.mesh import AppMesh
from lib.sfn import StepFunction
from lib.ecs import ECS
import time


class Canary(object):
    def __init__(self, params, logger):
        self.logger = logger
        self.params = params
        self.logger.info("Intiating Canary Process")
        self.logger.info(params)
        self.mesh = AppMesh(logger, mesh='test-mesh')
        self.ecs = ECS(logger)
        self.s3 = S3(logger)
        self.bucketname = 'EXAMPLE'

    

    def get_current_deployed_color(self):
        method = inspect.stack()[0][3]
        self.logger.info(f"Executing function {method}")
        ## CHANGE ALL THIS JUNK
        task_definition_information = self.ecs.describe_task_definition(Cluster=self.cluster, TaskDefinitioArn=self.task)
        # Query Cloudmap potientially for stack value we pass into tag!>
        current_color = 'blue'
        
        if current_color == 'blue':
            new_color == 'green'
        elif current_color == 'green':
            new_color == 'blue'
        else:
            self.logger.info("Ruh Roh got a valid color, but not blue or green")

        #OverWrite the current file with the one
        new_color_task_def = s3.download_file(f"task_def_{new_color}.json", self.bucketname)
        s3.upload_file("task_def.json", new_color_task_def, self.bucketname)


    def check_route_percentages(self, route, virtualNode):
        method = inspect.stack()[0][3]
        self.logger.info(f"Executing function {method}")
        try:
            response = self.mesh.describe_route(
                meshName=self.mesh, 
                routeName=route, 
                virtualRouterName=self.virtualRouter
            )
            for specs in response['route']['spec']['httpRoute']['action']['weightedTargets']:
                if specs['virtualNode'] == virtualNode:
                    self.route = route
                    self.route_spec  = response['route']['spec']
                else:
                    self.logger.info(f"Could not find matching virtual node target {virtualNode} for this route {route}")
            return route_weight
        except Exception as e:
            self.logger.error(f"Error performing {method}: {e}")

    def update_route_weight(self, desired_weight):
        method = inspect.stack()[0][3]
        self.logger.info(f"Executing function {method}")
        try:
            self.route_spec['httpRoute']['action']['weightedTargets'][0]['weight'] = int(desired_weight)
            if self.route_spec and self.route_weight is not None:
                self.mesh.update_route(
                    meshName = self.mesh
                    routeName = self.route
                    spec = self.route_spec
                    virtualNode = self.virtualRouter
                )
            else:
                self.logger.error('Recieved non valied arguements for route_spec, and route_weight')
        except Exception as e:
            self.logger.error(f"error running {method} ..... {e}")
