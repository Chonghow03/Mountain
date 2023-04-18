from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.linked_stack import LinkedStack
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')


class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241,
                   786433, 1572869]
    INTERNAL_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241,
                      786433, 1572869]
    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:
        if sizes is not None:
            self.TABLE_SIZES = sizes
        if internal_sizes is not None:
            self.INTERNAL_SIZES = internal_sizes
        self.size_index = 0

        self.top_level_table = LinearProbeTable(sizes)
        self.top_level_table.hash = lambda k: self.hash1(k)

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            # value = (ord(char) + a * value) % self.table_size
            # a = a * self.HASH_BASE % (self.table_size - 1)
            value = (ord(char) + a * value) % self.table_size()
            a = a * self.HASH_BASE % (self.table_size() - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        p1 = self.top_level_table._linear_probe(key1, is_insert)

        table = self.top_level_table.array[p1]
        if is_insert and table is None:
            table = LinearProbeTable(self.INTERNAL_SIZES)
            table.hash = lambda k: self.hash2(k, table)
            self.top_level_table[key1] = table
        else:
            table = table[1]
        p2 = table._linear_probe(key2, is_insert)
        return (p1, p2)

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        if key is None:
            for key in self.top_level_table.keys():
                yield key
        else:
            table = self.top_level_table[key]
            for key in table.keys():
                yield key

    def keys(self, key: K1 | None = None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        if key is None:
            return self.top_level_table.keys()
        else:
            table = self.top_level_table[key]
            return table.keys()

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        # raise NotImplementedError()
        if key is None:
            # get all tables' values
            tables = self.top_level_table.values()
            for t in tables:
                for value in t.values():
                    yield value
        else:
            table = self.top_level_table[key]
            for value in table.values():
                yield value

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        if key is None:
            # get all tables' values
            tables = self.top_level_table.values()
            values = []
            for t in tables:
                values += t.values()
            return values

        else:
            table = self.top_level_table[key]
            return table.values()

    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        try:
            position = self._linear_probe(key[0], key[1], False)
        except:
            raise KeyError(key)
        else:
            return self.top_level_table.array[position[0]][1].array[position[1]][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        try:
            position = self._linear_probe(key[0], key[1], True)
        except KeyError:
            self._rehash()
            self.__setitem__(key, data)  # try again
        else:
            self.top_level_table.array[position[0]][1][key[1]] = data

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        try:
            position = self._linear_probe(key[0],key[1],False)
        except:
            raise KeyError(key)
        else:
            del self.top_level_table.array[position[0]][1][key[1]]
            if self.top_level_table.array[position[0]][1].is_empty():
                self.top_level_table.array[position[0]] = None

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        raise NotImplementedError()

    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return self.TABLE_SIZES[self.size_index]

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        raise NotImplementedError()

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()


# if name
if __name__ == "__main__":
    """
    See spec sheet image for clarification.
    """
