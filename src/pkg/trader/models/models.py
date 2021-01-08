from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint
)
from sqlalchemy.ext.declarative import (
    as_declarative,
    declared_attr
)
from sqlalchemy.ext.hybrid import hybrid_property


@as_declarative()
class Model:
    id = Column(
        Integer,
        primary_key=True
    )

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


@as_declarative()
class Event:
    rate = Column(
        Numeric(32, 8),
        nullable=False
    )
    seq = Column(
        Integer,
        nullable=False
    )
    @declared_attr
    def exchange(self):
        return Column(Integer, ForeignKey('exchange.id'))

    @declared_attr
    def market(self):
        return Column(Integer, ForeignKey('market.id'))


class Exchange(Model):
    name = Column(
        String(64),
        unique=True,
        nullable=False
    )


class Market(Model):
    lhs = Column(
        String(16),
        nullable=False
    )
    rhs = Column(
        String(16),
        nullable=False
    )
    UniqueConstraint('lhs', 'rhs')

    @hybrid_property
    def name(self):
        return f'{self.lhs}_{self.rhs}'


class NewTrade(Model, Event):
    amount = Column(
        Numeric(32, 8),
        nullable=False
    )
    date = Column(
        DateTime(),
        nullable=False
    )
    total = Column(
        Numeric(32, 8),
        nullable=False
    )
    type = Column(
        String(16),
        nullable=False
    )


class OrderBookModify(Model, Event):
    amount = Column(
        Numeric(32, 8),
        nullable=False
    )
    type = Column(
        String(16),
        nullable=False
    )


class OrderBookRemove(Model, Event):
    pass
