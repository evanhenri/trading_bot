from datetime import datetime

from asyncpgsa import pg

from .. import models
from ..bases import Exchange
from ..store import db

from . import log


class PoloniexHandler:
    name = 'poloniex'
    ws_url = 'wss://api.poloniex.com'

    def __init__(self, dsn):
        self.dsn = dsn
        self.actions = {
            'newTrade'       : self._new_trade,
            'orderBookModify': self._order_book_modify,
            'orderBookRemove': self._order_book_remove
        }

    async def __aenter__(self):
        await pg.init(**self.dsn)
        self.exchange_id = await db.get_or_create(
            models.Exchange,
            column_num=0,
            name=self.name
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def __call__(self, *events, **kwargs):
        log.info(f'seq: {kwargs["seq"]}')

        if not events:
            return

        seq = kwargs['seq']
        lhs, rhs = kwargs['details'].topic.split('_')
        market_id = await db.get_or_create(
            models.Market,
            column_num=0,
            lhs=lhs,
            rhs=rhs,
        )
        for event in events:
            action = event['type']
            data   = event['data']
            await self.actions[action](
                exchange_id=self.exchange_id,
                market_id=market_id,
                seq=seq,
                **data
            )

    async def _new_trade(self, exchange_id, market_id, seq, **kwargs):
        log.info(f'new_trade: {kwargs}')
        return await db.create(
            models.NewTrade,
            exchange=exchange_id,
            market=market_id,
            seq=seq,
            amount=kwargs['amount'],
            date=datetime.strptime(kwargs['date'], '%Y-%m-%d %H:%M:%S'),
            rate=kwargs['rate'],
            total=kwargs['total'],
            type=kwargs['type']
        )

    async def _order_book_modify(self, exchange_id, market_id, seq, **kwargs):
        log.info(f'order_book_modify: {kwargs}')
        return await db.create(
            models.OrderBookModify,
            exchange=exchange_id,
            market=market_id,
            seq=seq,
            amount=kwargs['amount'],
            rate=kwargs['rate'],
            type=kwargs['type']
        )

    async def _order_book_remove(self, exchange_id, market_id, seq, **kwargs):
        log.info(f'order_book_remove: {kwargs}')
        return await db.create(
            models.OrderBookRemove,
            exchange=exchange_id,
            market=market_id,
            seq=seq,
            rate=kwargs['rate']
        )


class Poloniex(Exchange):
    @property
    def handler(self):
        return PoloniexHandler
