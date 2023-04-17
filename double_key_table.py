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
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        if sizes is not None:
            self.TABLE_SIZES = sizes
        if internal_sizes is not None:
            self.TABLE_SIZES = sizes
        self.size_index = 0
        self.top_level_table = LinearProbeTable(sizes)
        self.bottom_level_table = LinearProbeTable(sizes)

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
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
        position1 = self.hash1(key1)
        position2 = self.hash2(key2, self.bottom_level_table)

        for i in range(len(self.top_level_table)):
            if self.top_level_table[position1] is None:
                self.linear_prob_in_bottom(position1, position2, key2, is_insert)
            elif self.top_level_table[position1][0] == key1:
                self.linear_prob_in_bottom(position1, position2, key2, is_insert)
            else:
                position1 = (position1 + 1) % len(self.top_level_table)
        if is_insert:
            raise FullError("Top-level table is full!")
        else:
            raise KeyError(key1)

    def linear_prob_in_bottom(self, position1, position2, key2, is_insert):
        for j in range(len(self.top_level_table[position1])):
            if self.top_level_table[position1][1][position2] is None:
                return (position1, position2)
            elif self.top_level_table[position1][1][position2][0] == key2:
                return (position1, position2)
            else:
                position2 = (position2 + 1) % len(self.bottom_level_table)
        if is_insert:
            raise FullError("Bottom-level table is full!")
        else:
            raise KeyError(key2)

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """

    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        key_lst=[]
        if key == None:
            for i in range(len(self.top_level_table)):
                key_lst += self.top_level_table[i][0]
        else:
            for j in range(len(self.top_level_table[K1])):
                key_lst += self.top_level_table[K1][1][j][0]
        return key_lst


    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        raise NotImplementedError()

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        value_lst = []
        if key == None:
            for i in range(len(self.top_level_table)):
                value_lst += self.top_level_table[i][1]
        else:
            for j in range(len(self.top_level_table[K1])):
                value_lst += self.top_level_table[K1][1][j][1]
        return value_lst

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
        position1 = self.hash1(key[0])
        position2 = self.hash2(key[1], self.bottom_level_table)

        for i in range(len(self.top_level_table)):
            if self.top_level_table[position1] is None:
                raise KeyError(key[0])
            elif self.top_level_table[position1][0] == key[0]:
                for j in range(len(self.bottom_level_table)):
                    if self.top_level_table[position1][1][position2] is None:
                        raise KeyError(key[1])
                    elif self.top_level_table[position1][1][position2][0] == key[1]:
                        return self.top_level_table[position1][1][position2][1]
                    else:
                        position2 = (position2 + 1) % len(self.bottom_level_table)
                raise KeyError(key[1])
            else:
                position1 = (position1 + 1) % len(self.top_level_table)
        raise KeyError(key[1])


    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        position1 = self.hash1(key[0])
        position2 = self.hash2(key[1], self.bottom_level_table)

        for i in range(len(self.top_level_table)):
            if self.top_level_table[position1] is None:
                self.top_level_table[position1] = (key[0],self.bottom_level_table)
                self.set_item_in_bottom(position1,position2,key[1],data)

            elif self.top_level_table[position1][0] == key[0]:
                self.top_level_table[position1] = (key[0], self.bottom_level_table)
                self.set_item_in_bottom(position2,key[1],data)
            else:
                position1 = (position1 + 1) % len(self.top_level_table)

    def set_item_in_bottom(self, position1:int, position2:int, key, data) -> None:
        for j in range(len(self.top_level_table[position1][1])):
            if self.top_level_table[position1][1][position2] is None:
                self.top_level_table[position1][1][position2] = (key, data)
            elif self.top_level_table[position1][1][position2][0] == key:
                self.top_level_table[position1][1][position2] = (key, data)
            else:
                position = (position + 1) % len(self.bottom_level_table)
    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

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

