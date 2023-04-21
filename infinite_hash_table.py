from __future__ import annotations
from typing import Generic, TypeVar
from data_structures.hash_table import LinearProbeTable, FullError

from data_structures.linked_stack import LinkedStack

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
        # table_level = self.level  # current table level

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
        # print('----------\n', 'setting item: ', key, ' at level', table_level, ' at pos ', pos, 'with table', kv_pair)

        while kv_pair is not None:
            if type(kv_pair[1]) == InfiniteHashTable:
                step_into_table(kv_pair[1])
            else:
                # check if key is the same; if so, replace value
                if kv_pair[0] == key:
                    parent.array[pos] = (key, value)
                    return

                # already occupied by another key; create new table to resolve collision
                temp = kv_pair
                new_table = InfiniteHashTable(table_level)
                new_table.array[new_table.hash(temp[0])] = (temp[0], temp[1])
                new_table.count += 1
                # print('reinserted: ', temp[0], ' at level', table_level + 1, ' at pos ', new_table.hash(temp[0]),
                #       'with table', new_table.array[new_table.hash(temp[0])])
                # assign new table to parent, and set key as per instructions
                parent.array[pos] = (key[0:min(table_level, len(key))] + '*', new_table)
                step_into_table(new_table)

        # insert value
        parent.array[pos] = (key, value)
        parent.count += 1
        if parent is not self:
            self.count += 1
        # print('set item: ', key, ' at level', table_level, ' at pos ', pos, 'with table', kv_pair)

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """

        # if the level is 0, there is no need to delete
        # if the level is larger than 0, table must have more than one element

        table_to_collapse_to = self

        try:
            pos = self.get_location(key)
        except KeyError:
            raise KeyError('Key not found')
        else:
            table = self
            temp = None

            for i, p in enumerate(pos):

                if i == len(pos) - 1:  # second last table

                    for i, t in enumerate(table.array):
                        if t is not None:
                            print(i, t)
                    table.array[p] = None

                    table.count -= 1
                    if table.count == 1:
                        print('collapse')
                        temp = [kv_pair for kv_pair in table.array if kv_pair is not None][0]  # only one element left
                        if type(temp) == tuple:
                            if type(temp[1]) == InfiniteHashTable:
                                print('trigged')
                                table_to_collapse_to = None
                    else:
                        table_to_collapse_to = None
                    break

                if i> 0:
                    if table.count == 1:   # i must be > 0 as we do not collapse into parent table
                        if table_to_collapse_to is None:
                            table_to_collapse_to = table
                            print('trig')
                    else:
                        table_to_collapse_to = None
                print('current table: ', table_to_collapse_to, 'level: ', table.level)

                table = table.array[p][1]

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
                print('pos is ', pos)
                for i, t in enumerate(kv_pair[1].array):
                    if t is not None:
                        print(i, t)
                print('-----------')
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
    # def hashh(key, level=0):
    #     return ord(key[level]) % (27 - 1)
    #
    # print(hashh('lin'))
    # print(hashh('leg'))
    # print(hashh('lin', 1))
    # print(hashh('leg', 1))
    # print('---')
    ih = InfiniteHashTable()
    ih["lin"] = 1
    ih["leg"] = 2
    ih["mine"] = 3
    ih["linked"] = 4
    ih["limp"] = 5
    ih["mining"] = 6
    # ih["jake"] = 7
    ih["linger"] = 8

    # print(ih["mining"])
    del ih['limp']
    del ih["mine"]
    for i, t in enumerate(ih.array):
        if t is not None:
            print(i, t)
    print('-----------')
    print(ih.get_location('linger'))
    print('--')
    del ih['linger']
    print(ih.get_location('linger'))