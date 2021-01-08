from .. import bases


class CacheDSN(bases.DSN):
    @property
    def uri(self):
        return f'redis://{self["host"]}:{self["port"]}/0'
