import os
import ipaddr
import constants


class Settings(object):
    def __init__(self, base_path, network, mac_range):
        self._base_path = os.path.abspath(base_path)
        self.network = network
        self.mac_range = mac_range

    def base_path(self, *join_paths):
        return os.path.join(self._base_path, *join_paths)
    
    def overlays_path(self, *join_paths):
        return self.base_path(constants.OVERLAYS_DIR, *join_paths)

    def images_path(self, *join_paths):
        return self.base_path(constants.IMAGES_DIR, *join_paths)

    def skeletons_path(self, *join_paths):
        return self.base_path(constants.SKELETONS_DIR, *join_paths)
