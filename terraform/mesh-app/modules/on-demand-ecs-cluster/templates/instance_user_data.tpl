#! /bin/bash

# vim: ft=sh

set -euo pipefail

packages:uninstall(){
  yum erase -y 'ntp*'
}

packages:install() {
  yum install -y \
    awslogs \
    jq \
    tmux \
    chrony \
    amazon-ssm-agent
}


utils:install() {
  curl -fsSL -o /usr/local/bin/ec2-metadata https://gist.githubusercontent.com/n8foo/2830981/raw/2b76aa4799c06b0247e6e821fb1c451f611037e7/ec2-metadata.sh \
    && chmod 755 /usr/local/bin/ec2-metadata
}


configure:ecs-agent() {
  # Reference: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-config.html

  {
    echo "ECS_AVAILABLE_LOGGING_DRIVERS=[\"json-file\", \"splunk\", \"awslogs\"]"
    echo "ECS_CLUSTER=${cluster_name}"
    echo "ECS_ENABLE_CONTAINER_METADATA=true"
    echo "ECS_INSTANCE_ATTRIBUTES={ \"environment\": \"${environment}\" }"
  }
}


configure:awslogs() {
  # Reference: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_cloudwatch_logs.html#cwlogs_user_data

    cat > /etc/awslogs/awslogs.conf <<- EOF
    [general]
    state_file = /var/lib/awslogs/agent-state
    [general]
    state_file = /var/lib/awslogs/agent-state
    [/var/log/dmesg]
    file = /var/log/dmesg
    log_group_name = ${cloudwatch_prefix}/var/log/dmesg
    log_stream_name = ${cluster_name}/{instance_id}
    [/var/log/messages]
    file = /var/log/messages
    log_group_name = ${cloudwatch_prefix}/var/log/messages
    log_stream_name = ${cluster_name}/{instance_id}
    datetime_format = %b %d %H:%M:%S
    [/var/log/docker]
    file = /var/log/docker
    log_group_name = ${cloudwatch_prefix}/var/log/docker
    log_stream_name = ${cluster_name}/{instance_id}
    datetime_format = %Y-%m-%dT%H:%M:%S.%f
    [/var/log/ecs/ecs-init.log]
    file = /var/log/ecs/ecs-init.log.*
    log_group_name = ${cloudwatch_prefix}/var/log/ecs/ecs-init.log
    log_stream_name = ${cluster_name}/{instance_id}
    datetime_format = %Y-%m-%dT%H:%M:%SZ
    [/var/log/ecs/ecs-agent.log]
    file = /var/log/ecs/ecs-agent.log.*
    log_group_name = ${cloudwatch_prefix}/var/log/ecs/ecs-agent.log
    log_stream_name = ${cluster_name}/{instance_id}
    datetime_format = %Y-%m-%dT%H:%M:%SZ
    [/var/log/ecs/audit.log]
    file = /var/log/ecs/audit.log.*
    log_group_name = ${cloudwatch_prefix}/var/log/ecs/audit.log
    log_stream_name = ${cluster_name}/{instance_id}
    datetime_format = %Y-%m-%dT%H:%M:%SZ
EOF
}


configure:awslogs-destination-region() {
  # Set the region to send CloudWatch logs to (the region where the container instance is located)

  local awscli_conf="/etc/awslogs/awscli.conf"
  local local_az local_region
  local instance_id="$(curl 169.254.169.254/latest/meta-data/instance-id)"
  local_az="$(curl 169.254.169.254/latest/meta-data/placement/availability-zone)"
  local_region="$(sed s'/.$//' <<< "$local_az")"

  sed -i -e "s/region = us-east-1/region = $local_region/g" $awscli_conf
  sed -i -e "s/{instance_id}/$instance_id/g" /etc/awslogs/awslogs.conf
}


configure:container-instance-logging() {
  # Configures the CloudWatch Logs agent to start at every system boot

  cat <<-EOF
    #upstart-job
    description "Configure and start CloudWatch Logs agent on Amazon ECS container instance"
    author "Amazon Web Services"
    start on started ecs
    script
      exec 2> > /var/log/ecs/cloudwatch-logs-start.log
      set -x
      until curl -s http://localhost:51678/v1/metadata; do
        sleep 1
      done
      service awslogs start
      chkconfig awslogs on
    end script
EOF
}

packages:uninstall
packages:install
#utils:install

mkdir -p /etc/awslogs
configure:awslogs > /etc/awslogs/awslogs.conf
configure:awslogs-destination-region /etc/awslogs/awscli.conf
configure:ecs-agent > /etc/ecs/ecs.config
configure:container-instance-logging > /etc/init/awslogjob.conf

sed -i "s/server 169.254.169.123.*/server 169.254.169.123 prefer iburst minpoll 4 maxpoll 4/" /etc/chrony.conf
service chronyd start
chkconfig chronyd on

start ecs
start amazon-ssm-agent

echo "User data: Done"