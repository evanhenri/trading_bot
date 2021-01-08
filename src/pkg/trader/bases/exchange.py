import abc

from autobahn.asyncio import component
from autobahn.wamp.types import SubscribeOptions

from . import log


class Exchange:
    __metaclass__ = abc.ABCMeta

    @property
    @abc.abstractmethod
    def handler(self):
        raise NotImplementedError(
            '"handler" must be implemented as an inheriting class property'
        )

    def stream(self, dsn, market_patterns):
        log.info('stream: About to configure websocket component')
        websocket = component.Component(
            realm='realm1',
            transports=[{
                'url': self.handler.ws_url,
                'options': {
                    'fail_by_drop': True,
                    'open_handshake_timeout': 2500,
                    'close_handshake_timeout': 1000,
                    'auto_ping_interval': 10000,
                    'auto_ping_timeout': 5000,
                }
            }]
        )

        @websocket.on_connect
        async def connect(session, details):
            log.info(f'connect: {details}')

        @websocket.on_ready
        async def ready(session, details):
            log.info(f'ready: {details}')

        @websocket.on_join
        async def join(session, details):
            log.info(f'join: {details}')

            options = SubscribeOptions(
                details=True,
                match='prefix'
            )

            async with self.handler(dsn) as handler:
                for pattern in market_patterns:
                    await session.subscribe(
                        handler=handler,
                        options=options,
                        topic=pattern
                    )

        @websocket.on_leave
        async def leave(session, details):
            log.info(f'leave: {details}')

        @websocket.on_disconnect
        async def disconnect(session, details):
            log.info(f'disconnect: {details}')

        log.info(f'Connecting to {self.__class__.__name__} websocket API')
        component.run([websocket])
