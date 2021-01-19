from typing import Type, Optional, TypeVar, Callable, Union

from sqlalchemy import Table, Column, ForeignKey, Text, Index, Integer, Identity, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql.expression import or_

from .data_point import DataPoint
from .institute import Institute
from .model import Model
from .reading import Reading
from .researcher import Researcher
from .topic import Topic


def association_table(left: Type[DataPoint], right: Type[DataPoint], right_name: Optional[str] = None,
                      left_base_name: Optional[str] = None, left_plural: Optional[str] = None) -> Table:
    if not left_base_name:
        left_base_name = left.base_name
    if not left_plural:
        left_plural = left.plural
    if not right_name:
        right_name = right.plural

    new_table = Table(
        left_base_name + '_' + right_name,
        Model.metadata,
        Column(left.id.name, ForeignKey(left.id), primary_key=True),
        Column(right.id.name, ForeignKey(right.id), primary_key=True),
    )
    setattr(left, right_name, relationship(right, backref=left_plural, secondary=new_table))

    return new_table


class Affiliation(Model):
    __tablename__ = 'researcher_affiliations'
    id = Column('affiliation_id', Integer, Identity(always=True), primary_key=True)
    researcher_id = Column(ForeignKey(Researcher.id), nullable=False)
    institute_id = Column(ForeignKey(Institute.id), nullable=False)
    type = Column(Text, nullable=True)
    __table_args__ = (Index('affiliations_idx', researcher_id, institute_id, type, unique=True),)
    researcher = relationship(Researcher, backref="affiliations")
    institute = relationship(Institute, backref="affiliations")

    @classmethod
    def creator(cls: Type['Affiliation'], arg_name) -> Callable[[Model], 'Affiliation']:
        def the_creator(arg: Model) -> 'Affiliation':
            kwargs = {arg_name: arg}
            return cls(**kwargs)

        return the_creator


Researcher.institutes = association_proxy('affiliations', 'institute', creator=Affiliation.creator('institute'))
Institute.researchers = association_proxy('affiliations', 'researcher', creator=Affiliation.creator('researcher'))

reading1_id = Column('reading1_id', ForeignKey(Reading.id), primary_key=True)
reading2_id = Column('reading2_id', ForeignKey(Reading.id), primary_key=True)

reading_connections = Table('reading_connections', Model.metadata, reading1_id, reading2_id,
                            CheckConstraint('reading1_id != reading2_id'))

reading_topics = association_table(Reading, Topic)
researcher_readings = association_table(Researcher, Reading)
institute_readings = association_table(Institute, Reading)
