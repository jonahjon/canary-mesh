import requests  # used to make outbound requests e.g. URLget
from psutil import virtual_memory  # used to get memory statistics
from psutil import cpu_count  # used to get CPU counts
import os  # used to get environment Variables
import hashlib
import json
import logging

LOGGER = logging.getLogger(__name__)

class MainCommon:
    """
    Collection of helper functions to support the Basic ECS main app.
    """

    def __init__(self, app_name):
        """
        On initialization, pass in the app name that makes this unique, and get environment info.
         In AWS ECS environments, the task metadata URL is dynamic.  Example:
           ECS_CONTAINER_METADATA_URI="http://169.254.170.2/v3/5793e693-8833-4c53-a936-bcf40cff5f0a"
           https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-metadata-endpoint-v3.html
        :param app_name:
        """
        self.app_name = app_name

        self.metadata_url = os.environ.get('ECS_CONTAINER_METADATA_URI', '')
        LOGGER.info("Setting app name: [{}]".format(self.app_name))
        LOGGER.info("Setting container metadata URL: [{}]".format(self.metadata_url))

    def _convert_id_to_hex_color(self, instance_id):
        """
        Convert instance ID (or really any string) to hex
        :param instance_id:
        :return:
        """
        if not instance_id:
            instance_id = self.app_name
        m = hashlib.md5()
        m.update(instance_id.encode('utf-8'))
        hex_color = m.hexdigest()[:6]
        LOGGER.info("Converted instance ID [{}] to hex color #[{}]".format(instance_id, hex_color))
        return hex_color

    @staticmethod
    def _get_instance_stats():
        """
        Get information from the aws metadata service.
        :return: instance_id, instance_type
        """
        try:
            instance_id = requests.get('http://169.254.169.254/latest/meta-data/instance-id/', timeout=2).text
            instance_type = requests.get('http://169.254.169.254/latest/meta-data/instance-type/', timeout=2).text
        except Exception as e:
            LOGGER.error("Error calling task instance metadata. Exception: {}".format(e))
            instance_id = None
            instance_type = None
        return instance_id, instance_type

    def _get_container_stats(self):
        """
        This gets container metadata, if the app is running from AWS ECS.  Example response:
        {
            "DockerId": "bc4189f761edbddec81ef75b50baebd2991827a8b2178956345cea72afec5fe9",
            "Name": "service1",
            "DockerName": "ecs-service1-46-service1-e2a2e5b9eeead1d75900",
            "Image": "1234567890.dkr.ecr.us-west-2.amazonaws.com/demo-app:92d505",
            "ImageID": "sha256:43c2cffe831ca58807cb962b5cd112faefe2e0273e2b5c4bef0c7b1193d76a53",
            "Ports": [
                {
                    "ContainerPort": 80,
                    "Protocol": "tcp"
                }
            ],
            "Labels": {
                "com.amazonaws.ecs.cluster": "mycluster",
                "com.amazonaws.ecs.container-name": "service1",
                "com.amazonaws.ecs.task-arn": "arn:aws:ecs:us-west-2:1234567890:task/321ce4e1-9df0-4fcf-8352-c8221892ecac",
                "com.amazonaws.ecs.task-definition-family": "service1",
                "com.amazonaws.ecs.task-definition-version": "46"
            },
            "DesiredStatus": "RUNNING",
            "KnownStatus": "RUNNING",
            "Limits": {
                "CPU": 10,
                "Memory": 512
            },
            "CreatedAt": "2019-07-01T19:13:40.755779226Z",
            "StartedAt": "2019-07-01T19:13:42.9792103Z",
            "Type": "NORMAL",
            "Networks": [
                {
                    "NetworkMode": "bridge",
                    "IPv4Addresses": [
                        "172.17.0.10"
                    ]
                }
            ],
            "Volumes": [
                {
                    "Source": "/var/lib/ecs/data/metadata/3212e4e1-9df0-4fcf-8352-c8221895ecac/service1",
                    "Destination": "/opt/ecs/metadata/bcc7af6b-94ce-411a-b726-3e26df28ad48"
                }
            ]
        }
        """

        metadata = {}
        metadata['debug'] = {}
        metadata['debug']['metadata_url'] = self.metadata_url

        if self.metadata_url:
            try:
                task_metadata_raw = requests.get(self.metadata_url, timeout=2).text
                LOGGER.debug('Metadata Raw:')
                LOGGER.debug(json.dumps(task_metadata_raw))
                task_metadata = json.loads(task_metadata_raw)
                metadata['status'] = True
            except Exception as e:
                LOGGER.error("Error calling task metadata URL [{}]. Exception: {}".format(self.metadata_url, e))
                metadata['debug']['exception'] = e
                metadata['status'] = False
            # Build up a list of interesting metadata to return
            metadata["ecs_task_name"] = task_metadata.get("Name", "")
            metadata["ecr_image"] = task_metadata.get("Image", "")
            limits = task_metadata.get("Limits", {})
            metadata["task_cpu_limit"] = limits.get("CPU", "")
            metadata["task_mem_limit"] = limits.get("Memory", "")
            labels = task_metadata.get("Labels", {})
            metadata["cluster"] = labels.get("com.amazonaws.ecs.cluster", "")
            metadata["container_name"] = labels.get("com.amazonaws.ecs.container-name", "")

        else:
            LOGGER.error("Did not find metadata URL in the environment. Try running `echo $ECS_CONTAINER_METADATA_URI`")

        return metadata

    @staticmethod
    def _get_version():
        """
        This assumes a build system is updating the version.txt indide the app directory with a current value.
        :return: The contents of version.txt within the app root directory.
        """
        try:
            version_file = open(os.path.join('version.txt'))
            version = version_file.read().strip()
            LOGGER.info("Read version [{}] from version.txt".format(version))
        except Exception as e:
            LOGGER.error("Error reading version from file: version.txt", e)
            version = "UNKNOWN"
        return version

    def get_info(self):
        message = '<p>Hi, my name is <b>' + self.app_name + '</b>, version: <b>' + self._get_version() + '</b></p>'

        # AWS Instance Info
        instance_id, instance_type = self._get_instance_stats()
        if instance_id:
            message += '<p><b>I appear to be running on Amazon Web Services.</b></p>'
            message += '<div id=instance_stats>The instance I am running on is:<br />'
            message += '  Instance ID: <b>' + instance_id + '</b><br />'
            message += '  Instance Type: <b>' + instance_type + '</b><br />'
            message += '</div>'
        else:
            message += '<p>I cannot seem to hit the AWS metadata service.  Perhaps I am not running on AWS?</p>'

        # AWS ECS Container Info
        task_metadata = self._get_container_stats()
        LOGGER.info('Task Metadata')
        LOGGER.info(task_metadata)
        if task_metadata.get('status', False):
            message += '<div id=instance_stats>The ECS container I am running on is:<br />'
            message += '  Task Name: <b>' + task_metadata.get("ecs_task_name", "Not found") + '</b><br />'
            message += '  ECR Image: <b>' + task_metadata.get("ecr_image", "Not found") + '</b><br />'
            message += '  Task CPU Limit: <b>' + str(task_metadata.get("task_cpu_limit", "Not found")) + '</b><br />'
            message += '  Task Memory Limit: <b>' + str(task_metadata.get("task_mem_limit", "Not found")) + '</b><br />'
            message += '  ECS Cluster: <b>' + task_metadata.get("cluster", "Not found") + '</b><br />'
            message += '  Container Name: <b>' + task_metadata.get("container_name", "Not found") + '</b><br />'
            message += '</div>'
        else:
            message += '<p>I cannot seem to hit the ECS metadata service.  Perhaps I am not running on AWS ECS?</p>'

        bg_color = self._convert_id_to_hex_color(instance_id)

        # HTML headers for the response.
        response = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset=\"UTF-8\">
            <title>Where am I running?</title>
                <style>
        """
        response += "body {background-color: #" + bg_color + "; font: 1em \"Open Sans\", sans-serif;}"
        response += """
                </style>
        </head>
        <body>
        """

        response += message

        # Memory and CPUs
        mem = virtual_memory()
        memmegs =int(mem.total/(1024*1024))
        vcpu = cpu_count()
        pcpu = cpu_count(logical=False)
        response += '<div id=resources>I have access to <b>'+str(memmegs)+' MB of memory.</b><br/>'
        response += 'I have access to <b>'+str(vcpu)+' virtual CPUs.</b><br/>'
        response += 'I have access to <b>'+str(pcpu)+' physical CPUs.</b><br/>'
        response += '</div>'

        # close the HTML and return it (END OF INFO service)
        response += "</body>"
        response += "</html>"
        return response

    @staticmethod
    def get_route_frontend_file(app, path):
        # ...could be a static file needed by the front end that
        # doesn't use the `static` path (like in `<script src="bundle.js">`)
        file_path = os.path.join(app.static_folder, path)
        if os.path.isfile(file_path):
            return file_path
        # ...or should be handled by the SPA's "router" in front end
        else:
            return None