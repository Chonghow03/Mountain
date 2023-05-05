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
        """
        Initialise the Hash Table, and set the level.


        :complexity best: O(1)
        :complexity worst: O(1)
                - array: O(1)
                - set level: O(1)
                - set count: O(1)
        """

        self.array: ArrayR[tuple[K, V]] = ArrayR(self.TABLE_SIZE)
        self.level = level
        self.count = 0

    def hash(self, key: K) -> int:
        """
        Initialise the Hash Table, and set the level.


        :complexity: O(1) since we are only hashing one character
        best case is equal to worst case.
        """
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE - 1)
        return self.TABLE_SIZE - 1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        :complexity best: O(Comp(K)) when the position is a list with one element; that is; the element is in first table.
                    - get_location: O(Comp(K))
                    - get_table (for loop one time): O(1)
                    - get value: O(1)
        :complexity worst: O(M+Comp(K)) when the element is at the deepest level of the table, where M is the length of the key.
                    - get_location: O(Comp(K))
                    - get_table (for loop M-1 times): O(1)
                    - get value: O(1)
        This occurs when there exists a key with length M-1 in the table, causing M-1 tables to be traversed.
        """
        try:
            pos = self.get_location(key)  # O(1)
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
        We first define a helper function step_into_table that when called, sets the parent, pos, kv_pair, and table_level
        variables to the current table, the position of the key in the table, the key-value pair at that position,
        and the level of the table respectively.

        Overall Logic:
        1. We step into the top level table. - O(1)
        2. We check if the key is the same as the key in the table.  - O(comp(K))
        3. If it is, we replace the value then return  - O(1)
        4. If it isn't, we check if the value is a table.  - O(1)
        5. If the value is a table, we step into the table and repeat the process.
        best - O(1), where this doesn't happen
        worst - O(M), where we step inside for a total of M-1 times, where M is the length of the key
        6. Else, we create a new table, point old table to new table, and insert the key-value pair
        into the new table.  - O(1)

        :complexity best: O(comp(K)) when the key already exists in the top level table
                        - step into table: O(1)
                        - check if key is the same: O(comp(K))
                        - replace value: O(1)

        :complexity worst: O(M) when the element is at the deepest level of the table, where M is the length of the key;
        and we create new table to resolve the collision.
                        - step into table: O(1)
                        - step into table (M-1) times: O(M-1)
                        - create new table: O(1)
                        - assign new table to parent, and set key as per instructions: O(1)
                        - set key/value in new table: O(1)
                        - add 1 to count: O(1)
        """

        pos: int | None = None
        kv_pair: tuple[K, V] = (None, None)
        parent: InfiniteHashTable[K, V] | None = self
        table_level: int = self.level

        def step_into_table(table):
            """
            :complexity: O(1)
                - set parent: O(1)
                - hash key: O(1)
                - set kv_pair/ list access: O(1)
                - set table_level: O(1)
            """
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
                if kv_pair[0] == key:  # O(comp(K))
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

        This function is similar to __setitem__ in that it steps into the table to find the key. The core difference
        with del is that we need to collapse the table if there is only one element left in the table.
        We do this by storing a pointer to the table that we will collapse to, and the last element in the path that
        will be reinserted if collapse occurs.

        Overall Logic:
        1) We set the table_to_collapse_to to top level table. - O(1)
        2) We get the position of the key in the table. - O(1)
        3) We step into the table. - O(1)
        4) We check if the current table is the last table using level. - O(1)
        5) If it is, we delete the key-value pair by pointing to None. - O(1)
            6) Then, we check if the table has only one element left, and store it to temp - O(N)
            7) If temp is a table, we dont collapse. - O(1)
            8) BREAK out of the loop. - O(1)
        8) Else, if current table is collapsible, and if table_to_collapse is None, we try to set the table_to_collapse_to to the current
        table - O(1)
            9) Else, we set the table_to_collapse_to to None. - O(1)
        10) We step into the next table and repeat steps 4 to 10. - O(M)

        11) Finally, if table_to_collapse_to is not None, we collapse the table. - O(1)
        12) We store temp inside table_to_collapse_to. - O(1)

        :raises KeyError: when the key doesn't exist.

        :complexity best: O(Comp(K)) when the key is at the top level table, and there is no need to collapse.
                    - get_location: O(Comp(K)), where K is the length of the key
                    - step into table: O(1), when only step into top level table
                    - check if last table: O(1)
                    - delete key: O(1)
                    - for loop: O(1), when the remaining element is at the first index
                    - check if temp is table: O(1)
                    - break: O(1)


        :complexity worst: O(M+Comp(K)) when the key is at the deepest level of the table, where M is the length of the key;
                    - get_location: O(Comp(K)), where K is the length of the key
                    - step into table: O(M)
                    - check if last table: O(1)
                    - delete key: O(1)
                    - for loop: O(27) = O(1), when the remaining element is at the last index
                     (since size of alphabet is a constant, 26)
                    - check if temp is table: O(1)
                    - break: O(1)
                    -collapse table: O(1)
        """

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

        :complexity best: O(1)
        :complexity worst: O(1)
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.

        :complexity best: O(1)
        :complexity worst: O(1)
        """
        return str(self.array)

    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.

        :complexity best: O(Comp(K)) when the key is the first element in the table, and the table does not contain
        any extended tables.
                    - get_location: O(Comp(K))
                    - step into table: O(1), when only step into top level table
                    - check if key is equal: O(Comp(K))

        :complexity worst: O(M+Comp(K)) when the element is at the deepest level of the table, where M is the length of the key.
                    - get_location: O(1)
                    - step into table M-1 times: O(M)
                    - check if key is equal: O(Comp(K))

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
