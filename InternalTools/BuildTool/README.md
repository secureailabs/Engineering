Tapernak Build Tool

Tapernak allows users to easily build multiple projects which are dependant on one another.

# Terminology

    project
        - Any cpp project
    repository
        - Repository/root-folder containing all projects

# Node files

    build.node
        - these files describe how a project should be build and what it's dependencies are. Each build.node file contains the following
            - Identifier=<UUID>
                - The unique ID of the project
            - Dependency=<UUID>
                - UUID of another project which is required to be built beforehand (dependency)
                - There can be multiple dependencies
    build.root
        - used to determine the root of the repository containing all the projects
            - ex: /home/<USER>/ScratchPad/<USER>/build.root

# Arguments

    --all-nodes
        - All nodes specifies if Tapernak needs to find the root of the repository and build all projects inside of it
        - Default: false
        - If false, Tapernak will look for the build.node in the current working directory and only build that project and it's dependencies
