SHELL := /bin/bash
check: aws-cli-exists pip-exists j2-exists gnu-sed-exists
pip-exists: ; @which pip > /dev/null
aws-cli-exists: ; @aws --version > /dev/null
j2-exists: ; @which j2 > /dev/null
gnu-sed-exists: ; @which gsed > /dev/null
# Mac Install Commands
#pip install aws-cli
#pip install j2cli
#brew install gnu-sed

mytarget: check
.PHONY: check

sam: check
	chmod +x shell/sam.sh && ./shell/sam.sh

build:
	chmod +x shell/build.sh && ./shell/build.sh

terraform-up: check
	chmod +x shell/terraform.sh && ./shell/terraform.sh

destroy: check
	chmod +x shell/destroy.sh && ./shell/destroy.sh

deploy-files: check
	chmod +x shell/deploy.sh && ./shell/deploy.sh

watch: check
	chmod +x shell/watch.sh && ./shell/watch.sh

launch: check terraform-up deploy-files build




