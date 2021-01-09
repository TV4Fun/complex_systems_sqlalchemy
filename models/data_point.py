import typing

import inflection
import sqlalchemy
import sqlalchemy.orm

import models.model


class DataPoint(models.model.Model):
    def __init_subclass__(cls: typing.Type['DataPoint'], /, plural: typing.Optional[str] = None) -> None:
        super().__init_subclass__()
        cls.base_name = inflection.underscore(cls.__name__)
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
                foreign_key = sqlalchemy.Column(parent.base_name + '_id', sqlalchemy.ForeignKey(parent.id))
                setattr(cls, parent.id.name, foreign_key)
                setattr(cls, parent.base_name,
                        sqlalchemy.orm.relationship(parent, backref=cls.plural, foreign_keys=(foreign_key,)))
            else:
                raise TypeError("Did not recognize type of parent.")

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name=name, **kwargs)

    __abstract__ = True
    __parent_data_points__: typing.Collection[typing.Type['DataPoint']] = ()
    __tablename__: str
    id: sqlalchemy.Column
    name: sqlalchemy.Column
    plural: str
    base_name: str
