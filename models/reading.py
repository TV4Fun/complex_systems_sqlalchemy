from sqlalchemy import Column, Text
from sqlalchemy.orm import relationship

from util import SplitSet
from .data_point import DataPoint


class Reading(DataPoint):
    url = Column(Text)
    _left_connections = relationship('Reading', back_populates='_right_connections',
                                     secondary='reading_connections',
                                     primaryjoin="Reading.id == reading_connections.c.reading1_id",
                                     secondaryjoin="Reading.id == reading_connections.c.reading2_id",
                                     collection_class=set)
    _right_connections = relationship('Reading', back_populates='_left_connections',
                                      secondary='reading_connections',
                                      primaryjoin="Reading.id == reading_connections.c.reading2_id",
                                      secondaryjoin="Reading.id == reading_connections.c.reading1_id",
                                      collection_class=set)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connections = SplitSet(self._left_connections, self._right_connections)
