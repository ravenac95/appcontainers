import os


class AppContainerCreator(object):
    """Coordinates the creation of a new AppContainer"""
    def __init__(self, settings, app_container_cls, 
            lxc_service, file_assembler):
        self._settings = settings
        self._app_container_cls = app_container_cls
        self._lxc_service = lxc_service
        self._file_assembler = file_assembler

    def provision_container(self, base, reservation):
        """Provisions a brand new container
        
        :param base: An identifier for the base that we'd like to use
        :param type: str
        :param reservation: A ResourceReservation object that describes
            a container's resources
        """
        settings = self._settings
        app_container_cls = self._app_container_cls

        # Create the overlay director(y|ies)
        overlays = self._create_overlay_directories(reservation.name)

        # Create the LXC object
        lxc = self._create_lxc(reservation.name, base, overlays)

        # Setup the files in the LXC
        self._file_assembler.setup(settings, lxc, reservation)

        # Create and return an app container for the LXC and it's reservations
        return app_container_cls.create(base, lxc, reservation)

    def _create_overlay_directories(self, name):
        """Creates overlay directories"""
        top_overlay = self._settings.overlays_path(name)
        return [top_overlay]

    def _create_lxc(self, name, base, overlays):
        """Creates the LXC object from the given name and overlays"""
        return self._lxc_service.create(name, base=base, overlays=overlays)


class FileAssembler(object):
    def setup(self, settings, lxc, reservation):
        skeleton_path = settings.skeletons_path('base')
        lxc_path = lxc.path()
        writer = LXCSkeletonWriter(skeleton_path, lxc_path)
        # Walk the directory
        for root, dir_names, filenames in os.walk(skeleton_path):
            # Current relative path
            relative_root = os.path.relpath(root, skeleton_path)
            # Create directories
            for dir_name in dir_names:
                dir_path = os.path.join(relative_root, dir_name)
                writer.make_dir(dir_path)
            for filename in filenames:
                file_path = os.path.join(relative_root, filename)
                # If the file has '.tmpl' as an extension then run it
                # through the template renderer
                if filename.endswith('.tmpl'):
                    writer.render(file_path, lxc=lxc, settings=settings,
                            reservation=reservation)
                # Otherwise
                else:
                    # Copy the file
                    writer.copy(file_path)


class LXCSkeletonWriter(object):
    """Manages the writing of skeleton files to an LXC"""
    def __init__(self, skeleton_path, lxc_path):
        self.base_dir = skeleton_path
        self.lxc_path = lxc_path

    def render(self, path, **context):
        pass

    def copy(self, path):
        pass

    def make_dir(self, path):
        pass
