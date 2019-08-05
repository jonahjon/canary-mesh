import boto3
from lib.logger import Logger
from lib.mesh import AppMesh
import time

def lambda_logging(event, context):
    logger = Logger(loglevel='info')
    mesh_client = AppMesh(logger, mesh='test-mesh')
    client = boto3.client('appmesh', region_name='us-west-2')
    """
    Let's see how logging looks like for these too
    """
    start = time.time()
    for i in range(5):
        response = client.describe_mesh(
            meshName='test-mesh'
        )
        print(response)
    end = time.time()
    print ("Took old way %f seconds" % ((end - start)))

    logger.info("Switching methods to using Factory Method")

    start = time.time()
    for i in range(5):
        response = mesh_client.describe_mesh(mesh='test-mesh')
    end = time.time()
    print ("Took new way %f seconds" % ((end - start)))
