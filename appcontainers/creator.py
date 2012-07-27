import os
from .models import AppContainer, AncestorInfo
from .skeleton import SkeletonAssembler
from .directories import DirectoryList, Directory


def setup_app_container_creator(settings, lxc_service,
        app_container_cls=None, skeleton_assembler=None,
        ancestor_info_cls=None):
    """Wires together an appropriate AppContainerCreator"""
    # Perform default wiring if necessary
    skeleton_assembler = skeleton_assembler or SkeletonAssembler()
    app_container_cls = app_container_cls or AppContainer
    ancestor_info_cls = ancestor_info_cls or AncestorInfo

    return AppContainerCreator(settings, lxc_service,
            skeleton_assembler=skeleton_assembler,
            app_container_cls=app_container_cls,
            ancestor_info_cls=ancestor_info_cls)


class AppContainerCreator(object):
    """Coordinates the creation of a new AppContainer"""
    def __init__(self, settings, lxc_service, skeleton_assembler,
            app_container_cls, ancestor_info_cls):
        self._settings = settings
        self._app_container_cls = app_container_cls
        self._lxc_service = lxc_service
        self._skeleton_assembler = skeleton_assembler
        self._ancestor_info_cls = ancestor_info_cls

    def provision_container(self, base, reservation):
        """Provisions a brand new container

        :param base: An identifier for the base that we'd like to use
        :type base: str
        :param reservation: A ResourceReservation object that describes
            a container's resources
        """
        settings = self._settings
        app_container_cls = self._app_container_cls

        # Create the overlay directory
        overlay_directory = self._ensure_overlay_directory(reservation.name)

        # Create the LXC object
        lxc = self._create_lxc(reservation.name, base,
                overlays=[overlay_directory])

        # Setup the files in the LXC
        self._skeleton_assembler.setup(settings, lxc, reservation)

        # Setup ancestor info
        ancestor_info = self._ancestor_info_cls.create(base)

        # Create and return an app container
        return app_container_cls.create(ancestor_info, lxc, reservation)

    def _ensure_overlay_directory(self, name):
        """Creates overlay directory"""
        # FIXME messy right now
        overlay_path = self._settings.overlays_path(name)
        # Make the directory
        overlay_dir = Directory.make(overlay_path)
        return overlay_dir.path

    def _create_lxc(self, name, base, overlays):
        """Creates the LXC object from the given name and overlays"""
        return self._lxc_service.create(name, base=base, overlays=overlays)
