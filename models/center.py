from .data_point import DataPoint
from sqlalchemy import Column, Text
from .university import University


class Center(DataPoint):
    __parent_data_points__ = (University,)
    url = Column(Text)
    location = Column(Text)
