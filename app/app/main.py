from flask import Flask, send_file, request # used to live under flask
from main_common import MainCommon
from aws_xray_sdk.core import patch_all
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
import logging
import os

app = Flask(__name__)

app_name = os.environ.get('APP_NAME', '')

### XRAY ###
patch_all()
xray_recorder.configure(service="{}-apptracing".format(app_name))
XRayMiddleware(app, xray_recorder)

logging.basicConfig(level=logging.INFO, filename="main.log")
LOGGER = logging.getLogger("main")
PORT = 80
main_common = MainCommon(app_name)

with open("version.txt") as myfile:
    version="".join(line.rstrip() for line in myfile)

@app.route("/service-status") # e.g. health check
def servicestatus():
    return {'response': f"v{version}"}

@app.route("/") # if nothing specified, then return the static html page
def main():
    return main_common.get_info()

@app.route('/<path:path>')
def route_frontend(path):
    file = main_common.get_route_frontend_file(app, path)
    if not file:
        return "Not found :("
    else:
        return send_file(file)

if __name__ == "__main__":
    LOGGER.info("Starting ECS app on port [{}]".format(PORT))
    app.run(host="0.0.0.0", debug=True, port=PORT)