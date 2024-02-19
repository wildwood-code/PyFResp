from abc import ABC, abstractmethod
from typing import TypeAlias, Any
from ScaleShift import ScaleShift


StrList:       TypeAlias = list[str]
NumStrList:    TypeAlias = list[tuple[str, float]]
NumStrListI:   TypeAlias = list[list[tuple[str, float]]]
FloatList:     TypeAlias = list[float]
FloatTup:      TypeAlias = tuple[float, ...]
StrListI:      TypeAlias = list[list[str]]
FloatListI:    TypeAlias = list[list[float]]
FloatListTupI: TypeAlias = list[tuple[float, ...]]


class InstrumentSetting(ABC):

    def __init__(self) -> None:
        pass


    @property
    @abstractmethod
    def criteria(self) -> Any:
        pass


    @property
    @abstractmethod
    def value(self) -> Any:
        pass


    @value.setter
    @abstractmethod
    def value(self, value: Any) -> None:
        pass


class IndexedStringList(InstrumentSetting):
    """Indexed String List

    Initialize the list in the constructor by passing a list of string lists:
    The outer list is indexed. Each inner list represents the values which are
    valid for any given index. The index is 0-based.
    ex/ [["DC", "AC", "GND"]]
    The first value in each inner list is the default value for that index.
    Whenever the set value is changed, it is verified against the valid values
    for the current index. The last value for each index is stored.

    Properties:
    index - get or set
    criteria - get (returns valud list for current index)
    value - get or set
    """
    def __init__(self,
                 valid_list: StrListI,
                 index: int = None
                ) -> None:
        self._valid_list = []
        self._last_value = []
        for p in valid_list:
            self._valid_list.append(p)
            self._last_value.append(p[0])  # first item in each index is default
        if index is not None:
            self._index = index
        else:
            self._index = 0 # first set
        self._value = self._last_value[self._index]


    @property
    def index(self) -> int|None:
        return self._index


    @index.setter
    def index(self, index: int) -> None:
        is_success = False
        if isinstance(index, int):
            old_index = self._index
            if index >= 0 and index < len(self._valid_list):
                self._index = index
                if not index == old_index:
                    self._value = self._last_value[index]
                is_success = True
        if not is_success:
            raise Exception("Invalid index")


    @property
    def criteria(self) -> StrList:
        return self._valid_list[self._index]


    @property
    def value(self) -> str:
        return self._value


    @value.setter
    def value(self, value: str) -> None:
        if not isinstance(value, str):
            raise Exception("Value must be str")
        value = value.upper()
        is_valid_list = False
        for s in self._valid_list[self._index]:
            if value == s.upper():
                self._value = s
                is_valid_list = True
                self._last_value[self._index] = s
                break
        if not is_valid_list:
            raise Exception("Invalid value")


class StringList(InstrumentSetting):
    """String List

    Initialize the list in the constructor by passing a string lists:
    ex/ ["DC", "AC", "GND"]
    The first value in the list is the default value.

    Properties:
    criteria - get (returns valud list for current index)
    value - get or set
    """

    def __init__(self,
                 valid_list: StrList
                ) -> None:
        self._list = IndexedStringList([valid_list])


    @property
    def criteria(self) -> StrList:
        return self._list.criteria


    @property
    def value(self) -> str:
        return self._list.value


    @value.setter
    def value(self, value: str) -> None:
        self._list.value = value


class IndexedFloatRange(InstrumentSetting):
    """Indexed Float Range

    Initialize the ranges in the constructor by passing a list of lists of floats.
    The outer list is indexed. The index is 0-based.
    Each inner list represents the range of values and the default and may be
    passed as either a list or a tuple. The first value is the default.
    The second and third are the min and max (inclusive) defining the range.
    ex/ [(0.0, -10.0, 10.0), (0.0, -1.0, 1.0), (0.0, -0.1, 0.1)]
    Recommended format of inner is (default, min, max)
    Whenever the set value is changed, it is verified against the valid range
    for the current index. The last value for each index is stored.

    Properties:
    index - get or set
    criteria - get (returns valud list for current index)
    value - get or set
    """

    def __init__(self,
                 range: FloatListI|FloatListTupI,
                 index: int = None
                ) -> None:
        self._range = []
        for r in range:
            self._range.append([min(r), max(r), r[0]]) # min, max, default
        if index is not None:
            self._index = index
        else:
            self._index = 0 # first set
        self._value = self._range[self._index][2]  # default value for index


    @property
    def index(self) -> int|None:
        return self._index


    @index.setter
    def index(self, index: int) -> None:
        old_index = self._index
        if index >= 0 and index < len(self._range):
            self._index = index
            if not index == old_index:
                # index changed, so get new default or last value for index
                self._value = self._range[self._index][2]
        else:
            raise Exception("Invalid index")


    @property
    def criteria(self) -> FloatTup:
        return (self._range[self._index][0], self._range[self._index][1])


    @property
    def value(self) -> float:
        return self._value


    @value.setter
    def value(self, value: float) -> None:
        (xmin, xmax, _) = self._range[self._index]
        if value >= xmin and value <= xmax:
            self._value = value
            self._range[self._index][2] = value  # set last value for index
        else:
            raise Exception("Invalid value")


class FloatRange(InstrumentSetting):
    """Float Range

    The first value is the default. The second and third are the min and max
    (inclusive) defining the range.
    ex/ (0.0, -10.0, 10.0)
    Recommended format of inner is (default, min, max)

    Properties:
    index - get or set
    criteria - get
    value - get or set
    """

    def __init__(self,
                 range: FloatList|FloatTup
                ) -> None:
        self._range = IndexedFloatRange([range])


    @property
    def value(self) -> float:
        return self._range.value


    @property
    def criteria(self) -> FloatTup:
        return self._range.criteria


    @value.setter
    def value(self, value: float) -> None:
        self._range.value = value


class IndexedFloatStringList:

    _RELATIVE_TOL = 1.0e-6


    def __init__(self,
                 valid_list: NumStrListI,
                 index: int = None
                ) -> None:
        self._valid_list = []
        self._valid_float = []
        self._last_value = []
        for p in valid_list:
            my_list = [ t[0] for t in p ]
            my_float = [ t[1] for t in p ]
            self._valid_list.append(my_list)
            self._valid_float.append(my_float)
            self._last_value.append(my_list[0])  # first item in each index is default
        if index is not None:
            self._index = index
        else:
            self._index = 0 # first set
        self._value = self._last_value[self._index]


    @property
    def index(self) -> int|None:
        return self._index


    @index.setter
    def index(self, index: int) -> None:
        is_success = False
        if isinstance(index, int):
            old_index = self._index
            if index >= 0 and index < len(self._valid_list):
                self._index = index
                if not index == old_index:
                    self._value = self._last_value[index]
                is_success = True
        if not is_success:
            raise Exception("Invalid index")


    @property
    def criteria(self) -> StrList:
        return self._valid_list[self._index]


    def float_criteria(self):
        return self._valid_float


    @property
    def value(self) -> str:
        return self._value


    @value.setter
    def value(self, value: str|float|int) -> None:
        if isinstance(value, ScaleShift):
            # adjust scale up or down by shift value
            # find the current value and shift it, coercing within the valid range
            shift = int(value)   # scale adjustment
            value = self._value  # current value (we will search for it)
            my_idx = None
            for idx, v in enumerate(self._valid_list[self._index]):
                if value == v:
                    my_idx = idx
                    break
            if my_idx is not None:
                N = len(self._valid_list[self._index])
                my_idx = my_idx + shift
                if my_idx < 0:
                    my_idx = 0
                elif my_idx >= N:
                    my_idx = N-1
                value = self._valid_list[self._index][my_idx]
            else:
                raise Exception("Invalid value")

        if isinstance(value, str):
            # check for case-insensitive exact match
            value = value.upper()
            is_valid_list = False
            for s in self._valid_list[self._index]:
                if value == s.upper():
                    self._value = s
                    is_valid_list = True
                    break
            if not is_valid_list:
                # check for float equivalent
                value = float(value)  # TODO: use eng value decoder
                for i in range(len(self._valid_float[self._index])):
                    f = self._valid_float[self._index][i]
                    if f == 0.0:
                        if value == 0.0:
                            is_valid_list = True
                            self._value = self._valid_list[self._index][i]
                            break
                    else:
                        if abs((value-f)/f) <= IndexedFloatStringList._RELATIVE_TOL:
                            is_valid_list = True
                            self._value = self._valid_list[self._index][i]
                            break
                if not is_valid_list:
                    raise Exception("Invalid value")
        elif isinstance(value, float|int):
            value = float(value)
            is_valid_list = False
            for i in range(len(self._valid_float[self._index])):
                f = self._valid_float[self._index][i]
                if f == 0.0:
                    if value == 0.0:
                        is_valid_list = True
                        self._value = self._valid_list[self._index][i]
                        break
                else:
                    if abs((value-f)/f) <= IndexedFloatStringList._RELATIVE_TOL:
                        is_valid_list = True
                        self._value = self._valid_list[self._index][i]
                        break
            if not is_valid_list:
                raise Exception("Invalid value")
        else:
            raise Exception("Value must be str or float")


class FloatStringList:
    def __init__(self,
                 valid_list: NumStrList
                ) -> None:
        self._list = IndexedFloatStringList([valid_list])


    @property
    def criteria(self) -> StrList:
        return self._list.criteria


    @property
    def value(self) -> str:
        return self._list.value


    @value.setter
    def value(self, value: str|float) -> None:
        self._list.value = value


if __name__ == "__main__":
    # Test code

    A = StringList(["1", "2", "5", "10", "20", "50", "100"])
    print(A.criteria)
    A.value = "10"
    print(A.value)
    try:
        A.value = "30"
        print('FAILED! Did not catch invalid assignment A.value = "30"')
    except:
        print('Caught invalid assignment A.value = "30"')
    try:
        A.value = 5.0
        print('FAILED! Did not catch invalid assignment A.value = 5.0')
    except:
        print('Caught invalid assignment A.value = 5.0')

    B = FloatRange((0.0, -5.5, 5.5))
    print(B.criteria)
    B.value = 2.51
    print(B.value)
    try:
        B.value = 6.0
        print('FAILED! Did not catch out-of-range assignment')
    except:
        print("Caught out-of-range assignment")

    C = IndexedStringList([["1", "2", "5"], ["10", "20", "50"]])
    C.index = 1
    print(C.criteria)
    C.value = "20"
    print(C.value)
    try:
        C.value = "2"
        print('FAILED! Did not catch invalid assignment')
    except:
        print('Caught wrong index assignment C.value = "2"')
    C.index = 0
    print(C.criteria)
    print(C.value)

    D = IndexedFloatRange([(2.5, 0.0, 5.0), (0.0, -0.010, 0.10), (0.0, -0.1, 0.1)])
    D.index = 2
    print(D.criteria)
    D.value = 0.05
    print(D.value)
    try:
        D.value = -0.11
        print('FAILED! Did not catch out-of-range assignment')
    except:
        print('Caught out-of-range value assignment')
    D.index = 0
    print(D.value)

    E = IndexedFloatStringList([[("1m", 1.0e-3), ("2m", 2.0e-3), ("5m", 5.0e-3), ("10m", 10.0e-3), ("0", 0.0)], [("100m", 100.0e-3), ("200m", 200.0e-3), ("500m", 500.0e-3), ("1", 1.0), ("0", 0.0)]])
    print(E.criteria)
    print(E.index)
    E.value = "2m"
    print(E.value)
    E.value = "5.0e-3"
    print(E.value)
    E.value = 10.0e-3+1.0e-8
    print(E.value)
    try:
        E.value = 10.0e-3+1.0e-7
    except:
        print('Caught tolerance error')
    E.index = 1
    print(E.value)
    E.value = 0.5
    print(E.value)
    try:
        E.value = 10.0e-3
    except:
        print('Caught value with wrong index')

    F = IndexedFloatStringList([[("1m", 1.0e-3), ("2m", 2.0e-3), ("5m", 5.0e-3), ("10m", 10.0e-3), ("0", 0.0)]])
    print(F.criteria)
    F.value = "2m"
    print(F.value)
    F.value = "5.0e-3"
    print(F.value)
    F.value = 10.0e-3+1.0e-8
    print(F.value)
    try:
        F.value = 10.0e-3+1.0e-7
    except:
        print('Caught tolerance error')


# ******************************************************************************
#  Copyright © 2023 Kerry S. Martin, martin@wild-wood.net
#  Free for usage without warranty, expressed or implied; attribution required
# ******************************************************************************