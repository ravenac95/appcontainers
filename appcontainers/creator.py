import os
from .models import AppContainer
from .skeleton import SkeletonAssembler
from .directories import DirectoryList, Directory


def setup_app_container_creator(settings, lxc_service,
        app_container_cls=None, skeleton_assembler=None):
    skeleton_assembler = skeleton_assembler or SkeletonAssembler()
    app_container_cls = app_container_cls or AppContainer
    return AppContainerCreator(settings, lxc_service,
            skeleton_assembler=skeleton_assembler,
            app_container_cls=app_container_cls)


class AppContainerCreator(object):
    """Coordinates the creation of a new AppContainer"""
    def __init__(self, settings, lxc_service,
            skeleton_assembler, app_container_cls):
        self._settings = settings
        self._app_container_cls = app_container_cls
        self._lxc_service = lxc_service
        self._skeleton_assembler = skeleton_assembler

    def provision_container(self, base, reservation):
        """Provisions a brand new container

        :param base: An identifier for the base that we'd like to use
        :type base: str
        :param reservation: A ResourceReservation object that describes
            a container's resources
        """
        settings = self._settings
        app_container_cls = self._app_container_cls

        # Create the overlay director(y|ies)
        directory_list = self._create_directory_list(reservation.name)

        # Create the LXC object
        lxc = self._create_lxc(reservation.name, base,
                directory_list.as_paths())

        # Setup the files in the LXC
        self._skeleton_assembler.setup(settings, lxc, reservation)

        # Create and return an app container for the LXC and it's reservations
        return app_container_cls.create(base, lxc, reservation, directory_list)

    def _create_directory_list(self, name):
        """Creates overlay directories"""
        top_overlay = self._settings.overlays_path(name)
        # Make the directory
        overlay_dir = Directory.make(top_overlay)
        directory_list = DirectoryList([overlay_dir])
        return directory_list

    def _create_lxc(self, name, base, overlays):
        """Creates the LXC object from the given name and overlays"""
        return self._lxc_service.create(name, base=base, overlays=overlays)
