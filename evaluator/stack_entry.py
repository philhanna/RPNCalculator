from abc import ABC, abstractmethod

import mpmath


class StackEntry(ABC):
    def __init__(self, value=None):
        self._cls = StackEntry
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __eq__(self, other):
        return repr(self) == repr(other)

    @abstractmethod
    def __repr__(self):
        ...


class NumberEntry(StackEntry):
    def __init__(self, value):
        super().__init__(mpmath.mpf(value))

    def __repr__(self):
        sb = f"{NumberEntry.__name__}({self.value})"
        return sb