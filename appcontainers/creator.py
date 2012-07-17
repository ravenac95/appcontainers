import os
import tempita
import shutil
from .models import AppContainer

TEMPLATE_EXTENSION = '.tmpl'
TEMPLATE_EXTENSION_LENGTH = len(TEMPLATE_EXTENSION)


def setup_app_container_creator(settings, lxc_service,
        app_container_cls=None, file_assembler=None):
    file_assembler = file_assembler or FileAssembler()
    app_container_cls = app_container_cls or AppContainer
    return AppContainerCreator(settings, lxc_service,
            file_assembler=file_assembler,
            app_container_cls=app_container_cls)


class AppContainerCreator(object):
    """Coordinates the creation of a new AppContainer"""
    def __init__(self, settings, lxc_service,
            file_assembler, app_container_cls):
        self._settings = settings
        self._app_container_cls = app_container_cls
        self._lxc_service = lxc_service
        self._file_assembler = file_assembler

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
                writer.ensure_dir(dir_path)
            for filename in filenames:
                file_path = os.path.join(relative_root, filename)
                # If the file has '.tmpl' as an extension then run it
                # through the template renderer
                if filename.endswith(TEMPLATE_EXTENSION):
                    writer.render(file_path, lxc=lxc, settings=settings,
                            reservation=reservation)
                # Otherwise
                else:
                    # Copy the file
                    writer.copy(file_path)


class LXCSkeletonWriter(object):
    """Manages the writing of skeleton files and directory to an LXC"""
    def __init__(self, skeleton_base_path, lxc_base_path):
        self._skeleton_base_path = skeleton_base_path
        self._lxc_base_path = lxc_base_path

    def _generate_path_pair(self, path, remove_lxc_right=0):
        """Generates a path pair for the skeleton and lxc path

        :param path: a relative path for use in both skeleton and lxc
        :type path: str
        :param remove_lxc_right: characters to remove from the right on the lxc
            path
        :type remove_lxc_right: int
        """
        skeleton_path = os.path.join(self._skeleton_base_path, path)
        lxc_path = os.path.join(self._lxc_base_path, path[:-remove_lxc_right])

        return (skeleton_path, lxc_path)

    def render(self, path, **context):
        """Render a template in the skeleton into the LXC
        
        :param path: a relative path for use in both skeleton and lxc
        :type path: str
        :param context: the context for the templates
        """
        skeleton_file_path, lxc_file_path = self._generate_path_pair(path,
                TEMPLATE_EXTENSION_LENGTH)

        template = tempita.Template.from_filename(skeleton_file_path)

        rendered_data = template.substitute(**context)

        lxc_file = open(lxc_file_path, 'w')
        lxc_file.write(rendered_data)
        lxc_file.close()

    def copy(self, path):
        """Copy file from skeleton to lxc
        
        :param path: a relative path for use in both skeleton and lxc
        :type path: str
        """
        skeleton_file_path, lxc_file_path = self._generate_path_pair(path)
        shutil.copy(skeleton_file_path, lxc_file_path)

    def ensure_dir(self, path):
        """Ensure a directory that exists in the skeleton exists in the LXC
        
        :param path: a relative path for use in both skeleton and lxc
        :type path: str
        """
        skeleton_dir_path, lxc_dir_path = self._generate_path_pair(path)
        try:
            os.mkdir(lxc_dir_path)
        except OSError:
            # directory is already made no need to complain
            pass
