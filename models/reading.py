from sqlalchemy import Column, Text

from .data_point import DataPoint
from .researcher import Researcher


class Reading(DataPoint):
    url = Column(Text)
