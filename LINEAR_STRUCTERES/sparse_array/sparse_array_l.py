from typing import Any, Self, Optional
import copy


class SparseArrayList:
    def __init__(self, length: int, values: Optional[list[any]] = None, default_value: Any = 0) -> None:
        self._length = length
        self._default_value = default_value
        self._current = 0

        self._array = self._generate_array(values)

    def __str__(self) -> str:
        return f'SparseArrayList({self._array})'

    def __len__(self) -> int:
        return len(self.get_items())

    def __setitem__(self, key: int, value: Any) -> None:
        key = self._convert_item(key)

        if self._check_item(key):
            self._array[key] = value
        else:
            raise KeyError(f'your key is not in the division [0; {self._length})')

    def __getitem__(self, item: int) -> Any:
        item = self._convert_item(item)

        if self._check_item(item):
            return self._array[item]
        else:
            raise KeyError(f'your key is not in the division [0; {self._length})')

    def __eq__(self, other: Self) -> bool:
        if self._length != other._length:
            return False

        if self._array == other._array:
            return True

        return False

    def __iter__(self) -> Self:
        self._current = 0
        return self

    def __next__(self) -> Any:
        items = self.get_items()
        if self._current < len(items):
            cur_value = items[self._current]
            self._current += 1
            return cur_value
        else:
            raise StopIteration

    def _convert_item(self, item: int) -> int:
        if item < 0:
            return self._length + item

        return item

    def _check_item(self, item: int) -> bool:
        if 0 <= item < self._length:
            return True

        return False

    def _generate_array(self, values: Optional[list[any]]) -> list[Any]:
        if values:
            array = copy.deepcopy(values)

            if set_length := len(array) < self._length:
                for i in range(self._length - set_length - 1):
                    array.append(self._default_value)
            elif len(array) > self._length:
                raise ValueError('count of your values is higher than length')

            return array
        else:
            return [self._default_value for _ in range(self._length)]

    def get_items(self) -> list[Any]:
        return [item for item in self._array if item != self._default_value]

    def full_length(self):
        return self._length


if __name__ == "__main__":
    array1 = SparseArrayList(5, default_value=0)
    array2 = SparseArrayList(7, default_value=0)
    array3 = SparseArrayList(5, default_value=0)
    array4 = SparseArrayList(11, [1, 2, 3, 4, 5, 6, 0, 8], default_value=0)

    print(array1 == array3)
    print(array1 != array3)

    array1[0] = 1
    array1[-1] = 2
    array1[3] = 3
    array1[-4] = 4

    print(array1[2])
    print(array1[-2])

    print(array4)

    print(array1.get_items())

    for element in array1:
        print(element)
