from persistent.mapping import PersistentMapping
from .models import AppContainerMetadata
from .resources import available_name, available_mac, available_ip
from .repository import Repository


def setup_metadata_service(settings, repository, metadata_cls=None):
    metadata_cls = metadata_cls or AppContainerMetadata
    return AppContainerMetadataService(settings, repository,
            metadata_cls)


class AppContainerMetadataService(object):
    def __init__(self, settings, repository, metadata_cls=None):
        self._repository = repository
        self._settings = settings
        self._metadata_cls = metadata_cls

    def provision_metadata(self, base, image=None):
        metadatas = self._repository.all()

        # Arrays to track each used resource
        names = []
        ips = []
        macs = []

        # Collect used resources
        for metadata in metadatas:
            names.append(metadata.name)
            ips.append(metadata.ip)
            macs.append(metadata.mac)

        # Create random name (must be unique)
        name = available_name(names)

        # Reserve Free Resources
        ip = available_ip(ips, self._settings.network)
        mac = available_mac(macs, self._settings.mac_range)

        # Create appropriate ancester info
        metadata = self._metadata_cls.create(name, ip, mac, base, image)
        self._repository.save(metadata)
        return metadata


class AppContainerMetadataRepository(Repository):
    def all(self):
        """Returns a list of all metadata objects"""
        raw_metadatas = self._metadatas
        metadatas = map(lambda a: self._load(a[1]),
                raw_metadatas.items())
        return metadatas

    def find_by_name(self, name):
        raw_metadata = self._metadatas.get(name)
        if not raw_metadata:
            raise self.DoesNotExist('AppContainerMetadata "%s" does not exist'
                    % name)
        metadata = self._load(raw_metadata)
        return metadata

    def save(self, metadata):
        raw_metadatas = self._metadatas
        raw_metadatas[metadata.name] = PersistentMapping(
            name=metadata.name,
            ip=metadata.ip,
            mac=metadata.mac,
            base=metadata.base,
            image=metadata.image,
        )

    def delete(self, metadata):
        raw_metadatas = self._metadatas
        del raw_metadatas[metadata.name]

    @property
    def _metadatas(self):
        root_key = 'app_container_metadatas'
        raw_metadatas = self._database.root.get(root_key)
        if not raw_metadatas:
            raw_metadatas = PersistentMapping()
            self._database.root[root_key] = raw_metadatas
        return raw_metadatas

    def _load(self, raw_data):
        return AppContainerMetadata.create(raw_data['name'],
                raw_data['ip'], raw_data['mac'], raw_data['base'],
                raw_data['image'])
