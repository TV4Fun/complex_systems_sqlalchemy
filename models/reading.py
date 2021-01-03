from sqlalchemy import Column, Text

from .data_point import DataPoint
from .researcher import Researcher


class Reading(DataPoint):
    __parent_data_points__ = ((Researcher, 'author'),)
    url = Column(Text)
