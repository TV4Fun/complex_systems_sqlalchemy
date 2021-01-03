import typing

import sqlalchemy
import sqlalchemy.orm

import models.model


class DataPoint(models.model.Model):
    def __init_subclass__(cls: typing.Type['DataPoint'], /, plural: typing.Optional[str] = None) -> None:
        super().__init_subclass__()
        cls.base_name = cls.__name__.lower()
        if plural:
            cls.plural = plural
        else:
            cls.plural = cls.base_name + 's'

        cls.__tablename__ = cls.plural
        cls.id = sqlalchemy.Column(cls.base_name + '_id', sqlalchemy.Integer, sqlalchemy.Identity(always=True),
                                   primary_key=True)
        cls.name = sqlalchemy.Column(cls.base_name, sqlalchemy.Text, nullable=False, index=True, unique=True)
        for parent in cls.__parent_data_points__:
            if isinstance(parent, type) and issubclass(parent, DataPoint):
                setattr(cls, parent.id.name, sqlalchemy.Column(sqlalchemy.ForeignKey(parent.id)))
                setattr(cls, parent.base_name, sqlalchemy.orm.relationship(parent, backref=cls.plural))
            else:
                parent, parent_base_name = parent
                setattr(cls, parent_base_name + '_id', sqlalchemy.Column(sqlalchemy.ForeignKey(parent.id)))
                setattr(cls, parent_base_name, sqlalchemy.orm.relationship(parent, backref=cls.plural))

    __abstract__ = True
    __parent_data_points__: typing.Collection[
        typing.Union[typing.Type['DataPoint'], typing.Tuple[typing.Type['DataPoint'], str]]] = ()
    id: sqlalchemy.Column
    name: sqlalchemy.Column
    plural: str
    base_name: str
