import os
import tempita
import shutil

TEMPLATE_EXTENSION = '.tmpl'
TEMPLATE_EXTENSION_LENGTH = len(TEMPLATE_EXTENSION)


class SkeletonAssembler(object):
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
