import argparse
import logging
import sys

from trader.exchange import (
    Gemini,
    Poloniex
)
from trader.store import db

import settings


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(
    logging.StreamHandler(sys.stdout)
)


def parse_args():
    parser = argparse.ArgumentParser()

    # ex: main.py poloniex --patterns BTC_ ETH_
    parser.add_argument('exchange')
    parser.add_argument('--patterns', dest='market_patterns', nargs='+')

    return parser.parse_args()


def main():
    args = parse_args()

    dsn = db.DatabaseDSN(
        database=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASS,
        host=settings.DB_HOST,
        port=settings.DB_PORT
    )

    log.info('Populating database...')
    try:
        db.create_schema(uri=dsn.uri)
    except Exception as e:
        log.error(e)
    else:
        log.info('Populated database!')

    exchanges = {
        'gemini': Gemini,
        'poloniex': Poloniex
    }

    exchange = exchanges[args.exchange]()
    exchange.stream(
        dsn=dsn,
        market_patterns=args.market_patterns
    )


if __name__ == '__main__':
    main()
