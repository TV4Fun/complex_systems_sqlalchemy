from sqlalchemy import Column, Text

from .data_point import DataPoint


class University(DataPoint, plural='universities'):
    url = Column(Text)
    location = Column(Text)
