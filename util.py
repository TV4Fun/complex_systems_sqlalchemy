from itertools import chain
from typing import MutableSet, TypeVar, AbstractSet, Iterator

T = TypeVar('T')


class SplitSet(MutableSet[T]):
    def __init__(self, primary_set: MutableSet[T], *other_sets: MutableSet[T]):
        self.primary_set = primary_set
        self.other_sets = other_sets

    def __contains__(self, item: T) -> bool:
        return item in self.primary_set or any(item in s for s in self.other_sets)

    def __iter__(self) -> Iterator[T]:
        return chain(self.primary_set, *self.other_sets)

    def __len__(self) -> int:
        return len(self.primary_set) + sum(len(s) for s in self.other_sets)

    def __str__(self) -> str:
        return str(list(self))

    def add(self, value: T) -> None:
        if not any(value in s for s in self.other_sets):
            self.primary_set.add(value)

    def discard(self, value: T) -> None:
        self.primary_set.discard(value)
        for s in self.other_sets:
            s.discard(value)
