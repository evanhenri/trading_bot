import asyncio
import collections
import heapq
import time

from asyncpgsa import pg
import sqlalchemy as sa

from trader.store import db
from trader.models import (
    NewTrade,
    OrderBookModify
)

import logging
import sys
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(
    logging.StreamHandler(sys.stdout)
)


class Trainer:
    def __init__(self, dsn, market, elapsed_trades, usd_threshold):
        self.dsn = dsn
        self.market = market
        self.elapsed_trades = elapsed_trades
        self.usd_threshold = usd_threshold

    def __iter__(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            db.init_pg(self.dsn)
        )
        market_id = loop.run_until_complete(
            db.lookup_market_id(self.market)
        )

        seq_start = 0
        min_seq_heap = [seq_start]

        while True:
            if not min_seq_heap:
                time.sleep(2)
                continue

            windows = loop.run_until_complete(
                self.window_generator(
                    market_id,
                    seq_start,
                    self.elapsed_trades
                )
            )

            prior_seq_start = seq_start

            for order_book_activity, last_trade in windows:
                seq_start = last_trade['seq']
                yield order_book_activity, last_trade

            assert seq_start > prior_seq_start

    async def window_generator(self, market_id, seq_start, window_size):
        windows = []

        seq_end = await pg.fetchval(
            sa.select([
                sa.func.max(
                    NewTrade.seq
                )
            ]),
            column=0
        )

        range_q = sa.select([
            NewTrade,
            OrderBookModify
        ]).filter(
            NewTrade.market == OrderBookModify.market == market_id
        ).where(
            NewTrade.seq > seq_start
        ).order_by(
            'seq'
        ).limit(
            window_size
        )

        trade_range = await pg.fetch(
            range_q
        )


        sa.select([
            NewTrade
        ]).where(
            NewTrade.market == market_id
        ).where(
            NewTrade.seq > seq_start
        ).order_by(
            NewTrade.seq
        ).all()








        trade_range_min, trade_range_max = trade_range[0], trade_range[-1]

        order_book_activity_q = sa.select([
            OrderBookModify
        ]).where(
            sa.between(
                OrderBookModify.seq,
                trade_range_min['seq'],
                trade_range_max['seq']
            )
        ).order_by(
            OrderBookModify.seq
        )


        order_book_activity = await pg.fetch(
            order_book_activity_q
        )


        windows.append(
            (order_book_activity, last_trade)
        )

        return windows
