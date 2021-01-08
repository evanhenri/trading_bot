from datetime import datetime

from asyncpgsa import pg

from .. import models
from ..bases import Exchange
from ..store import db

from . import log


class GeminiHandler:
    name = 'gemini'
    ws_url = 'wss://api.gemini.com'

    def __init__(self, dsn):
        self.dsn = dsn

    async def __aenter__(self):
        log.info(f'attempting db connection using {self.dsn}')
        await pg.init(**self.dsn)
        self.exchange_id = await db.get_or_create(
            models.Exchange,
            column_num=0,
            name=self.name
        )
        log.info('db connected')
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def __call__(self, *events, **kwargs):
        log.info(f'seq: {kwargs["seq"]}')
        log.info(f'details: {kwargs["details"]}')

        # if not events:
        #     return

        # seq = kwargs['seq']
        lhs, rhs = kwargs['details'].topic.split('_')
        market_id = await db.get_or_create(
            models.Market,
            column_num=0,
            lhs=lhs,
            rhs=rhs,
        )
        for event in events:
            log.info(event)


class Gemini(Exchange):
    @property
    def handler(self):
        return GeminiHandler
