from sqlalchemy import Column, Text

from .data_point import DataPoint
from .university import University


class Researcher(DataPoint):
    __parent_data_points__ = (University,)
    email = Column(Text, unique=True, index=True)
    url = Column(Text)
