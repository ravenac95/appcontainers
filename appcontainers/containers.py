from .repository import Repository
from .models. import AppContainer, AncestorInfo


def setup_app_container_loader(lxc_service, resource_repository,
        app_container_cls=None, ancestor_info_cls=None):
    app_container_cls = app_container_cls or AppContainer
    ancestor_info_cls = ancestor_info_cls or AncestorInfo

    return AppContainerLoader(lxc_service, resource_repository,
            app_container_cls, ancestor_info_cls)


class AppContainerLoader(object):
    def __init__(self, lxc_service, resource_repository,
            app_container_cls, ancestor_info_cls):
        self._lxc_service = lxc_service
        self._resource_repository = resource_repository
        self._app_container_cls = app_container_cls
        self._ancestor_info_cls = ancestor_info_cls

    def load(self, raw_data):
        name = raw_data['name']
        raw_ancestor_info = raw_data['ancestor_info']
        # Get related reservation
        ancestor_info = self._ancestor_info_cls.create(**ancestor_info)

        # Load LXC
        lxc = self._lxc_service.get(name)

        # Get Reservation
        reservation = self._resource_repository.find_by_name(name)

        # Create the app_container
        return self._app_container_cls.create(ancestor_info, lxc, reservation)


class AppContainerRepository(Repository):
    def __init__(self, database, loader):
        super(AppContainerRepository, self).__init__(database)
        self._loader = loader

    @property
    def _app_containers(self):
        return self._database.root['app_containers']

    def all(self):
        raw_app_containers = self._app_containers
        app_containers = map(self._load, raw_app_containers.items())
        return app_containers

    def find_by_name(self, name):
        raw_app_container = self._app_containers.get(name)
        if not raw_app_container:
            raise self.DoesNotExist('AppContainer "%s" does not exist' % name)
        app_container = self._load(raw_app_container)
        return app_container

    def save(self, app_container):
        raw_app_containers = self._app_containers
        raw_app_containers[app_container.name] = dict(
            name=app_container.name,
            ancestor_info=dict(
                base=app_container.ancestor_info.base,
                image=app_container.ancestor_info.image,
            ),
        )

    def delete(self, app_container):
        raw_app_containers = self._app_containers
        del raw_app_containers[app_container.name]

    def _load(self, raw_data):
        return self._loader.load(raw_data)
