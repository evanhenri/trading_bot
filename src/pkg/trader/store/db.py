from asyncpgsa import pg
import sqlalchemy

from .. import bases
from ..models import (
    Market,
    Model
)


class DatabaseDSN(bases.DSN):
    @property
    def uri(self):
        return f'postgres://{self["user"]}:{self["password"]}@{self["host"]}:{self["port"]}/{self["database"]}'


def construct_select(model, **kwargs):
    q = sqlalchemy.select([model])
    for attr, value in kwargs.items():
        whereclause = getattr(model, attr).__eq__(value)
        q = q.where(whereclause)
    return q


async def create(model, column_num=None, **kwargs):
    q = sqlalchemy.insert(model, values=kwargs)
    if column_num is not None:
        return await pg.fetchval(q, column=column_num)
    return await pg.fetchrow(q)


def create_schema(uri):
    engine = sqlalchemy.create_engine(uri, echo=True)
    Model.metadata.create_all(engine)


async def first(model, column_num=None, **kwargs):
    q = construct_select(model, **kwargs)
    if column_num is not None:
        return await pg.fetchval(q, column=column_num)
    return await pg.fetchrow(q)


async def get_or_create(model, column_num=None, **kwargs):
    return (
        await first(model, column_num=column_num, **kwargs) or
        await create(model, column_num=column_num, **kwargs)
    )


async def init_pg(dsn):
    await pg.init(**dsn)


async def lookup_market_id(market):
    lhs, _, rhs = market.upper().partition('_')
    return await first(
        Market,
        lhs=lhs,
        rhs=rhs,
        column_num=0
    )
