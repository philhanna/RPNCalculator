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


class BooleanEntry(StackEntry):
    def __init__(self, value: bool):
        super().__init__(value)

    def __repr__(self):
        sb = f"{BooleanEntry.__name__}({self.value})"
        return sb


class HexEntry(StackEntry):
    def __init__(self, value: str):
        super().__init__(HexEntry.hex2dec(value))

    def __repr__(self):
        sb = f"{BooleanEntry.__name__}({self.value})"
        return sb

    @staticmethod
    def hex2dec(s: str) -> int:
        s = s.lower()
        if s[:2] == '0x':
            s = s[2:]
        total = 0
        for c in s:
            d = "0123456789abcdef".find(c)
            total *= 16
            total += d
        return total
        