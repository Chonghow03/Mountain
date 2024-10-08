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
          Arg:
          - sizes which is a list
          - internal_sizes which is a list

          Explain:
            - Initialise the Hash Table, setting the top level table as an ArrayR of size 5
            (first element in TABLE_SIZES).

          Complexity:
          - Worst case: O(1), all if statement and assignment are O(1) (constant time)
          - Best case: O(1), all if statement and assignment are O(1) (constant time)
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
           Explain:
           - Find the correct position for this key in the hash table using linear probing.

           Args:
           - key1 is the key of top level table
           - key2 is the key of bottom level table
           - is_insert is the boolean

           Raises:
           - KeyError: When the key pair is not in the table, but is_insert is False.
           - FullError: When a table is full and cannot be inserted.

           Returns:
           - result: A tuple of two integer.
           -  The first integer is the position of the top level table for key1.
           -  The second integer is the position of the bottom level table for key2.

           Complexity:
           - Worst Case: O((O(len(key1)) + N*comp(K)) * (O(len(key2)) + M*comp(K)))
                        - Let N be the table size of the top level table, M the table size of the bottom level table.
                        - The time complexity of hash1 is O(len(key1)) and hash2 is O(len(key2)).
                        - The for loop runs depend on table_size, thus the for loop runs N time (O(N)).
                        - Within the for loop, comp(K) is the complexity of comparing two keys.
                        - All the if statement, assignments, numerical operations and return statement are O(1).
                        - From the _linear_probe() function of hash_table, the worst case of time complexity is
                          (O(len(key2)) + M*comp(K)).

           - Best Case: O(hash1(key1) + hash2(key2))
                        - The time complexity of hash1 is O(len(key1)).
                        - When enter the condition of the key of the first obtained is equal to key1,
                        - the best case of _linear_probe() function in hash_table is O(hash(key2)).
                        - All the assignments, return statement, if statements are O(1).
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
           Explain:
            -Helper function to get the index of the inner table that contains the key using linear probing,
             with is_insert=True.

            -This works because rehashing for both top and inner tables are performed automatically,so the inner table
             is always non-full; implying we can reuse linear probing to find the correct index for top-level key by
             passing any key2 to the linear probing function, and then returning only position of inner table in top
             table.

           Args:
           - key is a string

           Returns:
           - result: An integer of index of top level table

           Complexity:
           - Worst Case: O(_linear_probe()) = O((O(len(key1)) + N*comp(K)) * (O(len(key2)) + M*comp(K)))
                         - Let N is the table size of the top level table, M is the table size of the bottom level table
                         - Comp(K) is the complexity of comparing two keys.
                         - Time complexity is the worst case of _linear_probe() function

           - Best Case: O(_linear_probe()) = O(hash1(key1) + hash2(key2))
                         - Time complexity is the best case of _linear_probe() function
        """
        return self._linear_probe(key, '_', True)[0]  # gets first element of tuple, which is the top-level key

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
           Explain:
           - When key = None, returns an iterator of all top-level keys in hash table
           - When key = k, returns an iterator of all keys in the bottom-hash-table for k.

           Args:
           - key is a string

           Returns:
           - result: An Iterator instance of Key1 type or Key2 type.

           Complexity: O(1), because it only returns an Iterator instance.
        """
        if key is None:
            return Iterator(self.top_level_table, Iterator.Scope.SINGLE, Iterator.IType.KEY)
        else:
            return Iterator(self.top_level_table[key][1].array, Iterator.Scope.SINGLE, Iterator.IType.KEY)

    def keys(self, key: K1 | None = None) -> list[K1]:
        """
           Explain:
           -key = None: returns all top-level keys in the table.
           -key = x: returns all bottom-level keys for top-level key x.

           Args:
           - key is a string

           Returns:
           - result: A list of all keys needed

           Complexity:
           - Worst Case: O(_linear_probe() * M) = O((len(key1)) + N*comp(K) * (len(key2) + M*comp(K) * M)
                        - Let N be the table size of the top level table, M the table size of the bottom level table.
                        - Comp(K) is the complexity of comparing two keys.
                        - When key is not None, since calling get_table_index() is worst case of O(linear_probing()),
                        - and then iterating through the bottom level table is O(M).
                        - All if, assignment, and return statements are O(1).

           - Best Case: O(N)
                       - When key is None, where N is table count.
                       - All if, assignment, and return statements are O(1).
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
           Explain:
           - key = None,returns an iterator of all values in hash table
           - key = k,returns an iterator of all values in the bottom-hash-table for k.

           Args:
           - key is a string

           Returns:
           - result: An Iterator instance of value type.

           Complexity: O(1), since it is just returning an iterator instance.
        """
        if key is None:
            return Iterator(self.top_level_table, Iterator.Scope.ALL, Iterator.IType.VALUE)
        else:
            return Iterator(self.top_level_table[key][1].array, Iterator.Scope.SINGLE, Iterator.IType.VALUE)

    def values(self, key: K1 | None = None) -> list[V]:
        """
           Explain:
           - key = None: returns all values in the table.
           - key = x: returns all values for top-level key x.

           Args:
           - key is a string

           Returns:
           - result: A list of all values needed

           Complexity:
           - Worst Case: O(N*M)
                        - When key is none, where N is the number of items in the top level table
                        - and M is the (average) number of items in the bottom level table.
                        - All assignments, if statements, return statement are constant time.

           - Best Case: O(hash1(key) * hash2(key) * N)
                        - when key is the first element of the first table, and that second position of the second
                          table is empty (best case for linear probing).
                        - N is the number of items in the table.
        """
        values = []

        def add_values(tab):
            for item in tab.array:
                if item is not None:
                    values.append(item[1])

        if key is None:
            for t in self.top_level_table:
                if t is None:
                    continue
                table = t[1]
                add_values(table)
        else:
            tables = [self.top_level_table[self._get_table_index(key)][1]]
            for table in tables:
                add_values(table)

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
           Explain:
           - Get the value at a certain key. First calls linear probing, then returns the value at the position.

           Args:
           - key is a tuple of key1 and key2.

           Returns:
           - result: The item in the table with provided key.

           Raises:
           - KeyError: when the key doesn't exist.

          Complexity:
           - Worst Case: O(_linear_probe()) = O((O(len(key1)) + N*comp(K)) * (O(len(key2)) + M*comp(K)))
                         - Let N be the table size of the top level table, M the table size of the bottom level table
                         - Comp(K) is the complexity of comparing two keys.
                         - All assignments and return statement are O(1).
                         - Thus the time complexity is depends on the worst case of _linear_probe function.

           - Best Case: O(_linear_probe()) = O(hash1(key1) + hash2(key2))
                         - All assignments and return statement are O(1).
                         - Thus the time complexity is depends on the best case of _linear_probe function.
        """
        try:
            position = self._linear_probe(key[0], key[1], False)
        except:
            raise KeyError(key)
        else:
            return self.top_level_table[position[0]][1].array[position[1]][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
           Explain:
           - Set an (key, value) pair in our hash table. First calls linear probing, then sets the value at the position
             by calling the __setitem__  function of the inner table.

           Args:
           - key is a tuple of key1 and key2.
           - data to store in the table.

           Returns:
           - None

           Complexity:
           - Worst Case: O((O(len(key1)) + N*comp(K)) * (O(len(key2)) + M*comp(K)) + hash2(key2)
                         + P * comp(K) + R * (O(len(key1)) + N*comp(K)) * (O(len(key2)) + M*comp(K)))

                        - The worst case time complexity of _linear_probe() is
                          O((O(len(key1)) + N*comp(K)) * (O(len(key2)) + M*comp(K))) where N is the table size of the
                          top level table, M is the table size of the bottom level table.
                        - The worst case time complexity of bottom_level_table.setitem() is
                          O(hash(key) + P*comp(K)) where P is the table size.
                        - The worst case time  complexity of _rehash() function is
                          O(R* _linear_probe()) where R is len(self)
                        - Comp(K) is the complexity of comparing two keys.


           - Best Case: O(hash1(key1) + hash2(key2) + hash2(key2))
                        - The best case time complexity of _linear_probe() is O(hash1(key1) + hash2(key2)).
                        - The best case time complexity of bottom_level_table.setitem() is O(hash2(key2)).
                        - All assignments are O(1) and for best case when len(self) <= self,table_size /2, so without
                          entering the if statement.
        """
        position = self._linear_probe(key[0], key[1], True)
        self.top_level_table[position[0]][1][key[1]] = data
        if len(self) > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
           Explain:
           - Deletes a (key, value) pair in our hash table.

           Args:
           - key is a tuple of key1 and key2

           Returns:
           - None

           Raises:
           - KeyError: when the key doesn't exist.

           Complexity:
           - Worst Case: O(O(len(key1)) + N*comp(K)) * (O(len(key2)) + M*comp(K)) + O(hash2(key2) + M*comp(K)) + O(N))
                        - Let N be the table size of the top level table, M the table size of the bottom level table.
                        - Comp(K) is the complexity of comparing two keys.
                        - The worst case time complexity of _linear_probe() is
                          O((O(len(key1)) + N*comp(K)) * (O(len(key2)) + M*comp(K))).
                        - The worst case time complexity of setitem of the bottom level table is O(hash2(key2) + M*comp(K))
                        - The time complexity of the while loop is O(N) where N is the size of top level table.
                        - All assignments, numerical operations and if statement are constant time.

           - Best Case: O(O(hash1(key1) + hash2(key2)) + O(hash2(key2)))
                        - When self.top_level_table[top_pos][1] is not empty
                        - The best case time complexity of _linear_probe() is O(hash1(key1) + hash2(key2)).
                        - The best case time complexity of setitem of the bottom level table is O(hash2(key2))
                        - All assignments and if statement are constant time.
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
            pos = self._get_table_index(key2)
            self.top_level_table[pos] = (key2, value)
            top_pos = (top_pos + 1) % self.table_size

    def _rehash(self) -> None:
        """
           Explain:
           - Need to resize table and reinsert all values. Reinserting uses linear probing to get top level key.

           Args:
           - None

           Return:
           - None

           Complexity:
           - Worst Case: O(N * _linear_probe()) = O(N * (O(len(key1)) + N*comp(K)) * (O(len(key2)) + M*comp(K)))
                         - Let N be the size of top level table
                         - The for loop iterate all the item in top level table, thus O(N).
                         - The worst case time complexity of _linear_probe() is
                           O((O(len(key1)) + N*comp(K)) * (O(len(key2)) + M*comp(K))).
                         - The worst case of setitem of arrayR is O(1).
                         - All assignments, if statement, numerical operation and return statement are O(1).

           - Best Case: O(1)
                        - When the size_index is equal to the length of TABLE_SIZES
                        - All assignments, if statement, numerical operation and return statement are O(1).
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
           Explain:
           - Return the current size of the table (different from the length)

           Args:
           - None

           Return:
           - An integer which is the length of top level table

           Complexity:
           - Worst Case: O(1), return statement

           - Best Case: O(1), return statement
        """
        return len(self.top_level_table)

    def __len__(self) -> int:
        """
           Explain:
           - Returns number of elements in the hash table

           Return:
           - An integer which is the count class variable.(how many item in the table)

           Complexity:
           - Worst Case: O(1), return statement

           - Best Case: O(1), return statement
        """
        return self.count

    def __str__(self) -> str:
        """
           Explain:
           - String representation.
           - Not required but may be a good testing tool.

           Return:
           - String of result

           Complexity:
           - Worst case: O(N), where N is the size of top level table (for loop).
                        - All assignments, if statement, numerical operation and return statement are O(1).

           - Best case: O(1), when nothing in top level table.
                        - All assignments, if statement, numerical operation and return statement are O(1).
        """
        result = ""
        for item in self.top_level_table:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + ", " + str(value) + ")\n"
        return result


class Iterator:
    """
    Iterator for the HashTable.

    Defines two Enum classes to determine the scope and type of the iterator.
    """
    class Scope(Enum):
        """
        Scope of the iterator.

        ALL: Iterate over all value/key pairs of all tables in the hash table.
        SINGLE: Iterate over all value/key pairs within a single table.
        """
        ALL = 1
        SINGLE = 2

    class IType(Enum):
        """
        Type of the value yield by iterator.

        KEY: Yield the key of the value/key pair.
        VALUE: Yield the value of the value/key pair.
        """
        KEY = 1
        VALUE = 2

    def __init__(self, table_array, scope: Scope, i_type: IType):
        """
           Explain:
           - Constructor for the Iterator class.

           Complexity: O(1)
                       - Best case = worst case = O(1)
                       - All assignments are constant time.

        """
        self.scope = scope
        self.type = i_type
        self.table_array = table_array
        self.i = 0

    def __iter__(self):
        """
           Explain:
           - Return the iterator object itself.

           Complexity: O(1)
                       - - Best case = worst case = O(1)
                       - Return statement is constant time.
        """
        return self

    def __next__(self):
        """
           Explain:
           - Returns the next item from the iterator. Depending on the scope of the iterator, it will either
            iterate over all the value/key pairs in all the tables or in a single table, incrementing the index self.i
            and the table index accordingly.

           Raises:
           - StopIteration: when there is no more item in the table(s)

           Returns:
           - the key or value of the next item in the table(s)

           Complexity:
           - Worst case: O (N * M), where N is the size of the table_array and M is the average size of the
           table_array[i]. This is the case when the iterator has scope ALL and the table_array is full, so the function
           goes through all the tables and all the items in each table.
                    - comparison: O(1)
                    - while loop: O(N)
                        - assignment: O(1)
                        - second while loop: O(M)
                            - get_item: O(1)
                            - yield: O(1)

           - Best case: O(N), where N is the size of the table_array. This is the case when the iterator
           has scope SINGLE. The function goes through all the items in only one table.
                    - comparison: O(1)
                    - while loop: O(N)
                        - comparison: O(1)
                        - get_item: O(1)
                        - yield: O(1)
        """
        def get_item(table_array, i):
            """
               Explain:
               - Helper function to get the item at index i in a given table_array. It returns the key or value
                depending on the type of the iterator.

               Returns:
               - result: the key or value at index i in the given table_array

               Complexity: O(1)
                        - All access, if, numerical operation and return statement are O(1).
            """
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
