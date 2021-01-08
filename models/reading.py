from sqlalchemy import Column, Text

from .data_point import DataPoint


class Reading(DataPoint):
    url = Column(Text)
