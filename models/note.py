from sqlalchemy import Column, Text

from .data_point import DataPoint
from .university import University
from .reading import Reading
from .topic import Topic
from .center import Center
from .researcher import Researcher


class Note(DataPoint):
    __parent_data_points__ = (Reading, Topic, Researcher, University, Center)
