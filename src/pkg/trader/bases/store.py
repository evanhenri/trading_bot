import abc
from collections.abc import Mapping


class DSN(Mapping):
    def __init__(self, **kwargs):
        self._dsn = kwargs

    def __iter__(self):
        yield from self._dsn

    def __getitem__(self, key):
        return self._dsn[key]

    def __len__(self):
        return len(self._dsn)

    @property
    @abc.abstractmethod
    def uri(self):
        pass
