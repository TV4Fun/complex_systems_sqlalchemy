from typing import Type, Optional

from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .data_point import DataPoint
from .model import Model
from .researcher import Researcher
from .center import Center
from .reading import Reading
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

        left_id = Column(left.id.name, ForeignKey(left.id), nullable=False)
        right_id = Column(right.id.name, ForeignKey(right.id), nullable=False)
        new_table = super().__new__(
            cls,
            left_base_name + '_' + right_name,
            Model.metadata,
            left_id,
            right_id,
            UniqueConstraint(left_id, right_id)
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
            self.right_id,
            UniqueConstraint(self.left_id, self.right_id)
        )
        setattr(left, self.right_name, relationship(right, backref=self.left_plural, secondary=self))

    left_base_name: str
    left_plural: str
    right_name: str
    left_id: Column
    right_id: Column


researcher_affiliations = AssociationTable(Researcher, Center, 'affiliations')
reading_topics = AssociationTable(Reading, Topic)
reading_citations = AssociationTable(Reading, Researcher, 'citations')
