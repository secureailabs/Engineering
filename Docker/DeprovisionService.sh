#!/bin/bash
set -e
ids=$(docker ps -aq --format "{{.Names}}")

PrintHelp()
{
    echo ""
    echo "Usage: $0 -s [Service Name]"
    echo -e "\t-s Service Name: all | devopsconsole | dataservices | platformservices | apiservices | webfrontend | orchestrator | remotedataconnector | securecomputationnode"
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
elif [ "$dockerContainer" == "all" ]
then
    echo "List of containers to be deprovisioned:"
    echo "-------------------------"
    docker ps -aq --format "{{.Names}}"
    echo "-------------------------"
    while true; do
        read -p "Are you sure you want to continue? " yn
        case $yn in
            [Yy] | [Yy][Ee][Ss] ) break;;
            [Nn] | [Nn][Oo] ) exit;;
            * ) echo "Please answer yes or no.";;
        esac
    done

    for id in $ids
    do
        echo "Stopping docker container :  "
        docker stop "$id"
        echo "Deprovisioning docker container :"
        docker rm "$id"
    done
    echo "!!! Deprovision Completed !!!"
    exit 0

fi

if [ "$dockerContainer" == "all" ]
then
    echo "Stopping $dockerContainer running containers ..."
    "docker kill $(docker ps -q)"
    echo "Deprovisioning $dockerContainer running containers ..."
    "docker rm $(docker ps -a -q)"
    echo "!!! Deprovision Completed !!!"
    exit 0
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
