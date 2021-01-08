from .data_point import DataPoint
from .institute import Institute
from .reading import Reading
from .researcher import Researcher
from .topic import Topic


class Note(DataPoint):
    __parent_data_points__ = (Reading, Topic, Researcher, Institute)
