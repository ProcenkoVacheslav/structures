import copy
from typing import Any, Optional, Self


class Array:
    def __init__(self, length: int, values: Optional[list[Any]] = None):
        self._length = length
        self._array = self._fill_array(values)
        self._current = 0

    def __str__(self):
        return f'Array({self._array})'

    def __setitem__(self, key: int, value: Any):
        key = self._get_key(key)
        if self._check_key(key):
            self._array[key] = value
        else:
            raise KeyError(f'your key is not in the division [0; {self._length})')

    def __getitem__(self, item: int):
        item = self._get_key(item)

        if self._check_key(item):
            return self._array[item]
        else:
            raise KeyError(f'your key is not in the division [0; {self._length})')

    def __eq__(self, other: Self):
        if self._length != other._length:
            return False

        if self._array == other._array:
            return True

        return False

    def __len__(self):
        return self._length

    @staticmethod
    def _check_length(length: int):
        if length <= 0:
            raise ValueError('length shuld be positive and not 0')

    @staticmethod
    def _check_value(value: Optional[list[Any]]):
        if not value:
            return False

        return True

    def _fill_array(self, values: Optional[list[Any]]):
        if self._check_value(values):
            array = copy.deepcopy(values)

            if set_length := len(array) < self._length:
                for i in range(self._length - set_length - 1):
                    array.append(None)
            elif len(array) > self._length:
                raise ValueError('count of your values is higher than length')

            return array
        else:
            return [None for _ in range(self._length)]

    def _check_key(self, key: int):
        if 0 <= key < self._length:
            return True

        return False

    def _get_key(self, key: int):
        if key < 0:
            return self._length + key

        return key

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        if self._current < self._length:
            cur_value = self._array[self._current]
            self._current += 1
            return cur_value
        else:
            raise StopIteration


if __name__ == "__main__":
    array1 = Array(5, ['a', 's', 'd', 'f', 'g'])
    array2 = Array(8)
    array3 = Array(5, ['a', 's', 'd', 'f', 'g'])
    array4 = Array(5, ['a', 's', 'd', 'f'])

    array2[-5] = 'b'
    array2[2] = 'e'

    exam1 = array2[-2]
    exam2 = array2[2]

    print(exam1)
    print(exam2)

    print(array2)
    print(array1 == array2)
    print(array1 == array3)
    print(array1 == array4)

    for element in array1:
        print(element)
