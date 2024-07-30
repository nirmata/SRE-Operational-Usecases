#!/bin/bash

podname="$2"
namespace="$1"
summary="Pod $podname restarting in $namespace namespace"
descriptiontext="Please find attached pod details for pod $podname in $namespace namespace"


python fetch-crashloopback-data.py $namespace $podname         
