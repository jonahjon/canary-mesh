#! /bin/bash

export $(xargs <.env)
export $(xargs <tf.env)


while sleep 3; do curl $dns_name/service-status && echo ''; done
