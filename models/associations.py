from typing import Type, Optional

from sqlalchemy import Table, Column, ForeignKey, Text
from sqlalchemy.orm import relationship

from .center import Center
from .data_point import DataPoint
from .model import Model
from .reading import Reading
from .researcher import Researcher
from .topic import Topic


class AssociationTable(Table):
    def __new__(cls, left: Type[DataPoint], right: Type[DataPoint], right_name: Optional[str] = None,
                left_base_name: Optional[str] = None, left_plural: Optional[str] = None) -> 'AssociationTable':
        if not left_base_name:
            left_base_name = left.base_name
        if not left_plural:
            left_plural = left.plural
        if not right_name:
            right_name = right.plural

        left_id = Column(left.id.name, ForeignKey(left.id), primary_key=True)
        right_id = Column(right.id.name, ForeignKey(right.id), primary_key=True)
        new_table = super().__new__(
            cls,
            left_base_name + '_' + right_name,
            Model.metadata,
            left_id,
            right_id
        )
        new_table.left_base_name = left_base_name
        new_table.left_plural = left_plural
        new_table.right_name = right_name
        new_table.left_id = left_id
        new_table.right_id = right_id

        return new_table

    def __init__(self, left: Type[DataPoint], right: Type[DataPoint], *_, **__) -> None:
        super().__init__(
            self.name,
            Model.metadata,
            self.left_id,
            self.right_id
        )
        setattr(left, self.right_name, relationship(right, backref=self.left_plural, secondary=self))

    left_base_name: str
    left_plural: str
    right_name: str
    left_id: Column
    right_id: Column


class Affiliation(Model):
    __tablename__ = 'researcher_affiliations'
    researcher_id = Column(ForeignKey(Researcher.id), primary_key=True)
    center_id = Column(ForeignKey(Center.id), primary_key=True)
    type = Column(Text)
    researcher = relationship(Researcher, backref="affiliations")
    center = relationship(Center, backref="affiliations")


reading_topics = AssociationTable(Reading, Topic)
researcher_readings = AssociationTable(Researcher, Reading)
center_readings = AssociationTable(Center, Reading)
