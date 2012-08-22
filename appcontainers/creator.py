from .models import AppContainer
from .skeleton import SkeletonAssembler
from .directories import Directory


def setup_app_container_creator(settings, lxc_service,
        app_container_cls=None, skeleton_assembler=None):
    """Wires together an appropriate AppContainerCreator"""
    # Perform default wiring if necessary
    skeleton_assembler = skeleton_assembler or SkeletonAssembler()
    app_container_cls = app_container_cls or AppContainer

    return AppContainerCreator(settings, lxc_service,
            skeleton_assembler=skeleton_assembler,
            app_container_cls=app_container_cls)


class AppContainerCreator(object):
    """Coordinates the creation of a new AppContainer"""
    def __init__(self, settings, lxc_service, skeleton_assembler,
            app_container_cls):
        self._settings = settings
        self._app_container_cls = app_container_cls
        self._lxc_service = lxc_service
        self._skeleton_assembler = skeleton_assembler

    def provision_container(self, metadata):
        """Provisions a brand new container

        :param metadata: An
            :class:`~appcontainers.creator.AppContainerMetadata` object
        """
        settings = self._settings
        app_container_cls = self._app_container_cls
        base = metadata.base
        name = metadata.name

        # Create the overlay directory
        overlay_directory = self._ensure_overlay_directory(name)

        # Create the LXC object
        lxc = self._create_lxc(name, base,
                overlays=[overlay_directory])

        # Setup the files in the LXC
        self._skeleton_assembler.setup(settings, lxc, metadata)

        # Create and return an app container
        return app_container_cls.create(lxc, metadata)

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
