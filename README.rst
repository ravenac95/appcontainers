appcontainers - a high level LXC utility
========================================

This builds, runs, and monitors App Containers and App Container images. App
Containers are used to sandbox arbitrary applications into an LXC.

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

Necessary Features
------------------

- Give out static IP addresses
- Generate random MAC addresses
- Save AppContainer images
- Load AppContainer images
- Add startup commands
- Run single commands
- Create files in the app container
- Base container tools

Directory Locations
-------------------

appcontainers stores information about the LXC's in the following locations by
default::

    - /var/lib/appcontainers/ - Root of appcontainers data
        - images/
            - bases/ - Base images
            - user/ - User loaded images
        - overlays/ - Stores overlay mounts / file systems here
            - tmp/ - Temporary overlays
            - image/ - Image overlays
            - raw/ - Raw overlays (this is not mounted nor squashed)
        - resources.json - Current state of the network resources
        - skeletons/ - Skeleton files for use in starting, provisioning, or
            loading containers. Tempita templates can be used here and the
            reservation object will be passed into the context
            

Possible use examples
---------------------

Create a new app container and load code into container's home directory::

    import appcontainers

    # Use defaults for the service
    app_container_service = appcontainers.setup_service() 
    
    # Provision the new container
    # After provisioning the container will have:
    #   - A static IP address
    #   - A unique MAC address (unique to this computer)
    new_container = app_container_service.provision()

    # Load data into the new container's home directory
    new_container.load_archive('path_to_archive.tar.gz')

    # Run one command in the container
    new_container.run('command')

    # ...
    # Blocks until the program is complete (this can never end)
    # ...

    # Once complete. Save to an image
    new_container.save_image('path_to_destination.aimg')

Load an app image::
    
    app_container_service = appcontainers.setup_service()
    
    # Load an image with an ephemeral file system
    loaded_container = app_container_service.load_image('path_to_image.aimg', 
        ephemeral=True)

    # Setup a startup command
    loaded_container.add_startup_command('command')

    # Start the container
    loaded_container.start()

    # Stop the container
    loaded_container.stop()
    
