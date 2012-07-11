appcontainers - a high level LXC utility
========================================

This builds, runs, and monitors App Containers and App Container images. App
Containers are used to sandbox arbitrary applications into an LXC.

Limitations
-----------

- Only one command can be run at one time (However, the command can still spawn
  multiple processes)
- Once a command has terminated the container is terminated

Host Requirements
-----------------

- Ubuntu 12.04
- ZeroMQ

LXC Requirements
----------------

The LXC's are required to have appcontainers-tools installed. This provides a
tool for stdout monitoring of commands that are run in the container.
Eventually it will also allow for input and output for commands run inside the
container.

Possible use examples
---------------------

Create a new app container and load code into container's home directory::

    import appcontainers

    # Use defaults for the service
    app_container_service = appcontainers.setup_service() 
    
    # Provision the new container
    # After provisioning the container will have:
    #   - A static IP address
    new_container = app_container_service.provision()

    # Load data into the new container's home directory
    new_container.load_archive('path_to_archive.tar.gz')

    # Run a command in the container
    new_container.run('command')


