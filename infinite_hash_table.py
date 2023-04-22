from __future__ import annotations
from typing import Generic, TypeVar
from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")


class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self, level=0) -> None:
        self.array: ArrayR[tuple[K, V]] = ArrayR(self.TABLE_SIZE)
        self.level = level
        self.count = 0

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE - 1)
        return self.TABLE_SIZE - 1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        try:
            pos = self.get_location(key)
        except KeyError:
            raise KeyError('Key not found')
        else:
            table = self
            for p in pos:
                table = table.array[p][1]
            return table

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        pos: int | None = None
        kv_pair: tuple[K, V] = (None, None)
        parent: InfiniteHashTable[K, V] | None = self
        table_level: int = self.level

        def step_into_table(table):
            nonlocal parent, pos, kv_pair, table_level
            parent = table
            pos = table.hash(key)
            kv_pair = table.array[pos]
            table_level += 1

        step_into_table(self)
        while kv_pair is not None:
            if isinstance(kv_pair[1], InfiniteHashTable):
                step_into_table(kv_pair[1])
            else:
                # check if key is the same; if so, replace value
                if kv_pair[0] == key:
                    parent.array[pos] = (key, value)
                    return

                # already occupied by another key; create new table to resolve collision
                new_table = InfiniteHashTable(table_level)
                new_table.array[new_table.hash(kv_pair[0])] = (kv_pair[0], kv_pair[1])
                new_table.count += 1
                # assign new table to parent, and set key as per instructions
                parent.array[pos] = (key[0:min(table_level, len(key))] + '*', new_table)

                step_into_table(new_table)

        # at correct table, set key
        parent.array[pos] = (key, value)
        parent.count += 1
        if parent is not self:
            self.count += 1

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """

        # if the level is 0, there is no need to delete
        # if the level is larger than 0, table must have more than one element

        table_to_collapse_to = self  # points to the table that we will eventually collapse to; if None, no collapse

        try:
            pos = self.get_location(key)
        except KeyError:
            raise KeyError('Key not found')
        else:
            table = self
            temp = None  # stores the last element in the path that will be reinserted if collapse occurs

            for level, p in enumerate(pos):
                if level == len(pos) - 1:  # last table
                    table.array[p] = None  # this is where we actually perform delete
                    table.count -= 1
                    if table.count == 1:
                        temp = [kv_pair for kv_pair in table.array if kv_pair is not None][0]  # find the only element left
                        if type(temp[1]) == InfiniteHashTable:
                            table_to_collapse_to = None
                    else:
                        table_to_collapse_to = None
                    break

                if level > 0:
                    if table.count == 1:   # i must be > 0 as we do not collapse into parent table
                        if table_to_collapse_to is None:
                            table_to_collapse_to = table
                    else:
                        table_to_collapse_to = None

                table = table.array[p][1]  # step into next table

            if table_to_collapse_to is not None and len(pos) > 1:
                table_to_collapse_to.array[table_to_collapse_to.hash(temp[0])] = (temp[0], temp[1])
            if table is not self:
                self.count -= 1

    def __len__(self):
        """
        Returns the number of elements in the hash table.
        """
        print('count is: ', self.count)
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        # for i, t in enumerate(ih.array):
        #     if t is not None:
        #         print(i, t)
        #
        # values = []
        return str(self.array)

    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        pos = self.hash(key)
        kv_pair = self.array[pos]
        path = [pos]

        while kv_pair is not None:
            if type(kv_pair[1]) == InfiniteHashTable:
                pos = kv_pair[1].hash(key)
                kv_pair = kv_pair[1].array[pos]
                path.append(pos)
            else:
                if kv_pair[0] == key:
                    return path
                raise KeyError('Key not found')
        raise KeyError()  # not found

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True


if __name__ == '__main__':
    pass
