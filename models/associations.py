from typing import Type, Optional

from sqlalchemy import Table, Column, ForeignKey, Text, Index, Integer, Identity
from sqlalchemy.orm import relationship

from .data_point import DataPoint
from .institute import Institute
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
    id = Column('affiliation_id', Integer, Identity(always=True), primary_key=True)
    researcher_id = Column(ForeignKey(Researcher.id), nullable=False)
    institute_id = Column(ForeignKey(Institute.id), nullable=False)
    type = Column(Text, nullable=True)
    __table_args__ = (Index('affiliations_idx', researcher_id, institute_id, type, unique=True),)
    researcher = relationship(Researcher, backref="affiliations")
    institute = relationship(Institute, backref="affiliations")


# class ReadingConnection(Model):
#    __tablename__ = 'reading_connections'
#    reading1_id = Column('reading1_id', ForeignKey(Reading.id), primary_key=True)
#    reading2_id = Column('reading2_id', ForeignKey(Reading.id), primary_key=True)


reading_topics = AssociationTable(Reading, Topic)
researcher_readings = AssociationTable(Researcher, Reading)
institute_readings = AssociationTable(Institute, Reading)
