from .models import AppContainer


def setup_app_container_loader(settings, lxc_service, app_container_cls=None):
    app_container_cls = app_container_cls or AppContainer

    return AppContainerLoader(settings, lxc_service, app_container_cls)


class AppContainerLoader(object):
    """Loads active app containers"""
    def __init__(self, settings, lxc_service, app_container_cls):
        self._settings = settings
        self._app_container_cls = app_container_cls
        self._lxc_service = lxc_service

    def load_container(self, metadata):
        name = metadata.name
        lxc = self._lxc_service.get(name)
        return self._app_container_cls.create(lxc, metadata)
