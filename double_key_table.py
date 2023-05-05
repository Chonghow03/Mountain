from __future__ import annotations

from enum import Enum
from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
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
        """
          Explain:
          -

          Args:
          -

          Raises:
          -

          Returns:
          - result:

          Complexity:
          - Worst case:
          - Best case:
        """
        if sizes is not None:
            self.TABLE_SIZES = sizes
        if internal_sizes is not None:
            self.INTERNAL_SIZES = internal_sizes

        self.size_index = 0
        self.count = 0
        self.top_level_table: ArrayR[tuple[K1, V]] = ArrayR(self.TABLE_SIZES[self.size_index])

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

        :complexity best: O(hash1(key) * hash2(key)) when the first position of the first table is empty,
                            and the second table exists AND that first position of the second table is empty.
        :complexity worst: O((hash(key) + N*comp(K)) * (hash2(key) + M*comp(K)))
                        when we've searched the entirety of both tables,
                        where N is the tablesize of the first table, M is the tablesize of the second table,
                        and comp(K) is the complexity of comparing two keys.
        """
        top_pos = self.hash1(key1)
        for _ in range(self.table_size):
            if self.top_level_table[top_pos] is None:
                if is_insert:
                    table = LinearProbeTable(self.INTERNAL_SIZES)
                    table.hash = lambda k: self.hash2(k, table)
                    self.top_level_table[top_pos] = (key1, table)
                    self.count += 1
                    bottom_pos = table._linear_probe(key2, is_insert)
                    return top_pos, bottom_pos
                else:
                    raise KeyError(key1)
            elif self.top_level_table[top_pos][0] == key1:
                bottom_pos = self.top_level_table[top_pos][1]._linear_probe(key2, is_insert)
                return top_pos, bottom_pos
            else:
                top_pos = (top_pos + 1) % self.table_size
        if is_insert:
            raise FullError("Table is full!")
        else:
            raise KeyError()

    def _get_table_index(self, key):
        """
        Helper function to get the index of the inner table that contains the key using linear probing,
        with is_insert=True.

        This works because rehashing for both top and inner tables are performed automatically,
        so the inner table is always non-full; implying we can reuse linear probing to
        find the correct index for top-level key by passing any key2 to the linear probing function, and then
        returning only position of inner table in top table.

        :complexity best: O(linear_probing())
        :complexity worst: O(linear_probing())
        """
        return self._linear_probe(key, '_', True)[0]  # gets first element of tuple, which is the top-level key

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.

        :complexity best: O()
        :complexity worst: O()
        """
        if key is None:
            return Iterator(self.top_level_table, Iterator.Scope.SINGLE, Iterator.IType.KEY)
        else:
            return Iterator(self.top_level_table[key][1].array, Iterator.Scope.SINGLE, Iterator.IType.KEY)

    def keys(self, key: K1 | None = None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        :complexity best: O(N) when key is None, where N is table count.
        :complexity worst: O(linear_probing() * N) when key is not None, since calling get_table_index()
        is O(linear_probing()), and then iterating through the inner table is O(N).
        """
        keys = []
        if key is None:
            table = self.top_level_table
        else:
            table = self.top_level_table[self._get_table_index(key)][1].array
        for item in table:
            if item is not None:
                keys.append(item[0])
        return keys

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        :complexity best: O()
        :complexity worst: O()
        """
        if key is None:
            return Iterator(self.top_level_table, Iterator.Scope.ALL, Iterator.IType.VALUE)
        else:
            return Iterator(self.top_level_table[key][1].array, Iterator.Scope.SINGLE, Iterator.IType.VALUE)

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        :complexity best: O(hash1(key) * hash2(key) * N) when key is the first element of the first table, and that
        second position of the second table is empty (best case for linear probing).
        N is the number of items in the table.

        :complexity worst: when key is none O(N*M) where N is the number of items in the table and M is
        the (average) number of items in the inner table.
        """

        values = []
        if key is None:
            tables = [t[1] for t in self.top_level_table if t is not None]
        else:
            tables = [self.top_level_table[self._get_table_index(key)][1]]
        for table in tables:
            for item in table.array:
                if item is not None:
                    values.append(item[1])
        return values

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
        Get the value at a certain key. First calls linear probing, then returns the value at the position.

        :raises KeyError: when the key doesn't exist.

        :complexity best: O(linear_probing())
        :complexity worst: O(linear_probing())
        """
        try:
            position = self._linear_probe(key[0], key[1], False)
        except:
            raise KeyError(key)
        else:
            return self.top_level_table[position[0]][1].array[position[1]][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table. First calls linear probing, then sets the value at the position.
        by calling the __setitem__  function of the inner table.

        :complexity best: O(linear_probing() * inner_table.setitem())
        :complexity worst: O() where rehash occurs after setting the item.
        """
        position = self._linear_probe(key[0], key[1], True)
        self.top_level_table[position[0]][1][key[1]] = data
        if len(self) > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        :complexity best: O()
        :complexity worst: O()
        """
        top_pos, bottom_pos = self._linear_probe(key[0], key[1], False)

        # auto handle internal table deletion
        del self.top_level_table[top_pos][1][key[1]]

        # return if internal table is not empty; no need to relocate
        if not self.top_level_table[top_pos][1].is_empty():
            return

        self.top_level_table[top_pos] = None
        top_pos = (top_pos + 1) % self.table_size

        while self.top_level_table[top_pos] is not None:
            key2, value = self.top_level_table[top_pos]
            self.top_level_table[top_pos] = None
            # Reinsert.
            pos = self._get_table_index(key2)  # todo: check this
            self.top_level_table[pos] = (key2, value)
            top_pos = (top_pos + 1) % self.table_size

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values. Reinserting uses linear probing to get top level key.

        :complexity best: O(N * linear_probing()) No probing.
        :complexity worst: O(N* linear_probing()) Worst case for linear probing.
        Where N is len(self)
        """

        old_array = self.top_level_table
        self.size_index += 1
        if self.size_index == len(self.TABLE_SIZES):
            return
        self.top_level_table = ArrayR(self.TABLE_SIZES[self.size_index])
        for item in old_array:
            if item is not None:
                key, value = item
                self.top_level_table[self._get_table_index(key)] = item

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)

        :complexity best: O(1)
        :complexity worst: O(1)
        """
        return len(self.top_level_table)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table

        :complexity best: O(1)
        :complexity worst: O(1)
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        result = ""
        for item in self.top_level_table:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result


class Iterator:
    class Scope(Enum):
        ALL = 1
        SINGLE = 2

    class IType(Enum):
        KEY = 1
        VALUE = 2

    def __init__(self, table_array, scope: Scope, i_type: IType):
        self.scope = scope
        self.type = i_type
        self.table_array = table_array
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        def get_item(table_array, i):
            item = table_array[i]
            if self.type is self.IType.KEY:
                return item[0]
            elif self.type is self.IType.VALUE:
                return item[1]

        if self.scope is self.Scope.ALL:
            self.table_index = 0
            while self.table_index < len(self.table_array):
                if self.table_array[self.table_index]:
                    bottom_table_array = self.table_array[self.table_index][1].array
                    while self.i < len(bottom_table_array):
                        if bottom_table_array[self.i]:
                            return get_item(bottom_table_array, self.i)
                        self.i += 1
                    self.i = 0  # resets i when we move to next table
                self.table_index += 1  # move to next table

        elif self.scope is self.Scope.SINGLE:
            while self.i < len(self.table_array):
                if self.table_array[self.i]:
                    return get_item(self.table_array, self.i)
                self.i += 1

        raise StopIteration


if __name__ == "__main__":
    """
    See spec sheet image for clarification.
    """
