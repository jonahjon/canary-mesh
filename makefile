SHELL := /bin/bash
check: jq-exists aws-cli-exists pip-exists j2-exists
pip-exists: ; @which pip > /dev/null
aws-cli-exists: ; @aws --version > /dev/null
jq-exists: ; @which jq > /dev/null
j2-exists: ; @which j2 > /dev/null
sam-exists: ; @sam --version > /dev/null
#pip install aws-cli
#brew install jq
#pip install j2cli
#brew install sam

mytarget: check
.PHONY: check #build

sam: check
	chmod +x sam.sh && ./sam.sh


