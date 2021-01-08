from typing import Type

from sqlalchemy import Column, Text, ForeignKey

from .data_point import DataPoint


class Institute(DataPoint):
    """
    Abstract class for a university or other kind of research institute
    """

    def __init_subclass__(cls: Type['Institute'], **kwargs):
        super().__init_subclass__(**kwargs)
        cls.id = Column(Institute.id.name, ForeignKey(Institute.id), primary_key=True)
        del cls.name
        cls.__mapper_args__ = {
            'polymorphic_identity': cls.base_name,
        }

    url = Column(Text)
    location = Column(Text)
    type = Column(Text)

    __mapper_args__ = {
        'polymorphic_identity': 'institute',
        'polymorphic_on': type
    }
