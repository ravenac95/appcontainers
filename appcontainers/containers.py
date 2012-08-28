from .repository import Repository


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
