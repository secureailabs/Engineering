#!/bin/bash
set -e

PrintHelp()
{
    echo ""
    echo "Usage: $0 -s [Service Name]"
    echo -e "\t-s Service Name: platformservices | dataservices | orchestrator | remotedataconnector | webfrontend | securecomputationnode"
    exit 1 # Exit script after printing help
}

while getopts "hs:" opt
do
    case "$opt" in
        s ) dockerContainer="$OPTARG" ;;
        ? ) PrintHelp ;;
    esac
done

# Print Help in case parameters are not correct
if [ -z "$dockerContainer" ]
then
    PrintHelp
fi

# Check if the docker container is running | stopped
containerRunning=$(docker ps --filter name="$dockerContainer" --format '{{.Image}}')
containerStopped=$(docker ps -a --filter name="$dockerContainer" --format '{{.Image}}')
if [ "$containerRunning" == "$dockerContainer" ]
then
    echo "!!! Docker container $dockerContainer is currently running !!!"
    echo "Stopping $dockerContainer ..."
    docker stop "$(docker ps -q --filter ancestor="$dockerContainer")"
    echo "Deprovisioning $dockerContainer ..."
    docker rm "$(docker ps -a -q --filter ancestor="$dockerContainer")"
    echo "!!! Deprovision Completed !!!"
    exit 0
elif [ "$containerStopped" == "$dockerContainer" ]
then
    echo "!!! Docker container $dockerContainer is currently stopped !!!"
    echo "Deprovisioning $dockerContainer ..."
    docker rm "$(docker ps -a -q --filter ancestor="$dockerContainer")"
    echo "!!! Deprovision Completed !!!"
    exit 0
else
    echo "!!! Docker Container $dockerContainer is already deprovisioned !!!"
fi
