[![.github/workflows/build.yml](https://github.com/secureailabs/Engineering/actions/workflows/build.yml/badge.svg)](https://github.com/secureailabs/Engineering/actions/workflows/build.yml)
[![.github/workflows/build.yml](https://github.com/secureailabs/Engineering/actions/workflows/build-c-cpp.yml/badge.svg)](https://github.com/secureailabs/Engineering/actions/workflows/build-c-cpp.yml)
![alt text](https://github.com/secureailabs/Engineering/blob/main/Logo.jpg?raw=true)


# Engineering
This is where the source code for all internal and external facing artifacts get maintained and built.

## Building for source

Open a terminal and clone the git repository:
```sh
$ git clone https://github.com/secureailabs/Engineering.git
```

## For a full end-to-end deployment
Download the datascience repository which is added as a submodule to this repository
```sh
git submodule update --init
```

## Building Binaries
From root of Repository run the following commands to build and verify Binaries

```
make clean
make all -j
```
Outputs:
```
ll -lrt Binary/
```

## DeployPlatform to Azure
DeployPlatform is required to run behind SAIL VPN. \
Please ensure connection to `vnet-sail-wus-hub-001` and have access to SAIL private vnets in Azure \

Set environment variables in deploy_config.sh to use `Deploy Platform Service Principal` - Ask Stanley if unclear \
`AZURE_SUBSCRIPTION_ID` should reflect the Azure Subscription you wish to deploy your resources in.
```
export AZURE_SUBSCRIPTION_ID="xxxx"
export AZURE_TENANT_ID="xxxx"
export AZURE_CLIENT_ID="xxxx"
export AZURE_CLIENT_SECRET="xxxx"
export AZURE_OBJECT_ID="xxxx"
export DOCKER_REGISTRY_URL="xxx"
export DOCKER_REGISTRY_USERNAME="xxx"
export DOCKER_REGISTRY_PASSWORD="xxx"
```
One can optionally update the version of the docker container images to be used for deployment by changin the x_TAG variables in deploy_config.sh with the required version.
Build image using the Docker/BuildImage.sh script and copy the tag from the result of the build. Update the deploy_config.sh with the tag.
If everything works, feel free to update the default values in the script.

Run the DeployPlatform script with `--help` for guidance
```
./DeplayPlatform.sh --help
```

## DeployPlatform locally with Docker
There is a readme under `Docker/`
Please see the documentation


# Release Process

1. Create a new branch from master
2. Upgrade the version in the `VERSION` file. e.g. from 0.1.0 to 0.2.0 according to [semantic versioning](https://semver.org/)
3. Commit the changes and push the branch to github
4. Run the github action [Create Container Images](https://github.com/secureailabs/Engineering/actions/workflows/wf_dispatch_create_container_images.yml) for all the services from this branch. Note the generated tag.
5. Update the `deploy_config.sh` file with the new tags
6. Push the new changes to github on same branch
7. Run all the tests and QA on this branch
8. Tag the branch with the new version. e.g. `git tag -a v0.2.0 -m "Version 0.2.0"`
9. Create a PR which will trigger `ci_pr_main.yml` which will run end2end in Development Subscription
10. Push the tag to github. e.g. `git push origin v0.2.0`
11. Once every thing works, merge the branch to main
12. Merge to main will trigger `ci_push_main_update_doc.yml` which updates github pages for api documentation
13. A long living staging environment can then be created from major version releases in Release Candidate Subscription to be used for long term tests and possible for sales demos via a manual trigger of `wf_dispatch_deploy_platform.yml`
