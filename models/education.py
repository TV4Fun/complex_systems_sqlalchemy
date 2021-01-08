from sqlalchemy import Column, Integer

from .data_point import DataPoint
from .degree import Degree
from .researcher import Researcher
from .topic import Topic
from .university import University


class Education(DataPoint):
    __parent_data_points__ = (University, Researcher, Topic, Degree)
    year = Column(Integer)
