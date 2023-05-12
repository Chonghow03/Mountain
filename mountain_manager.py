from algorithms.mergesort import mergesort
from double_key_table import DoubleKeyTable
from mountain import Mountain


class MountainManager:
    """
    MountainManager acts as a store for mountains, and provides methods to add, remove and edit mountains.

    Mountains are stored in a double key hash table, with the difficulty level as the first key and the mountain name
    as the second key. This allows for efficient lookup of mountains by difficulty level and name.
    The property of double key table means that our implementation automatically groups mountains by difficulty level
    (key1), and allows for efficient lookup of mountains by name (key2).
   """

    def __init__(self) -> None:
        """
         Explain:
           - Initialise a Double Key Hash Table self.organisers, which stores a list of tuple ('difficulty', Mountain)

         Complexity:
         - Worst case: O(1), assignment is O(1) (constant time)
         - Best case: O(1), assignment is O(1) (constant time)
        """
        self.organisers = DoubleKeyTable()

    def add_mountain(self, mountain: Mountain):
        """
          Arg:
          - mountain: Mountain to be added to the MountainManager

          Explain:
            - add the mountain into the hash table according to their difficulty_level as the key.

          Complexity:
          - Worst case: O(DoubleKeyTable(setitem))(worst) = O((O(len(key1)) + N*comp(K)) * (O(len(key2)) + M*comp(K))
                        + hash2(key2) + P * comp(K) + R * (O(len(key1)) + N*comp(K)) * (O(len(key2)) + M*comp(K)))

                        - In this function just add the mountain into the hash table by using the setitem function of
                          DoubleKeyTable.
                        - The worst case time complexity of _linear_probe() is
                          O((O(len(key1)) + N*comp(K)) * (O(len(key2)) + M*comp(K))) where N is the table size of the
                          top level table, M is the table size of the bottom level table.
                        - The worst case time complexity of bottom_level_table.setitem() is
                          O(hash(key) + P*comp(K)) where P is the table size.
                        - The worst case time  complexity of _rehash() function is
                          O(R* _linear_probe()) where R is len(self)
                        - Comp(K) is the complexity of comparing two keys.

          - Best case:  O(DoubleKeyTable(setitem))(best) = O(hash1(key1) + hash2(key2) + hash2(key2))

                        - The best case time complexity of _linear_probe() is O(hash1(key1) + hash2(key2)).
                        - The best case time complexity of bottom_level_table.setitem() is O(hash2(key2)).
                        - All assignments are O(1) and for best case when len(self) <= self,table_size /2, so without
                          entering the if statement.
        """
        self.organisers[str(mountain.difficulty_level), mountain.name] = mountain

    def remove_mountain(self, mountain: Mountain):
        """
          Arg:
          - mountain: Mountain to be removed from the Hash Table

          Explain:
           - delete the mountain in the hash table by finding their correct position

          Complexity:
          - Worst case: O(DoubleKeyTable(delitem))(worst) =
                        O(O(len(key1)) + N*comp(K)) * (O(len(key2)) + M*comp(K)) + O(hash2(key2) + M*comp(K)) + O(N))

                        - Let N be the table size of the top level table, M the table size of the bottom level table.
                        - Comp(K) is the complexity of comparing two keys.
                        - The worst case time complexity of _linear_probe() is
                          O((O(len(key1)) + N*comp(K)) * (O(len(key2)) + M*comp(K))).
                        - The worst case time complexity of setitem of the bottom level table is O(hash2(key2) + M*comp(K))
                        - The time complexity of the while loop is O(N) where N is the size of top level table.
                        - All assignments, numerical operations and if statement are constant time.

          - Best case: O(DoubleKeyTable(delitem))(best) = O(O(hash1(key1) + hash2(key2)) + O(hash2(key2)))

                        - When self.top_level_table[top_pos][1] is not empty
                        - The best case time complexity of _linear_probe() is O(hash1(key1) + hash2(key2)).
                        - The best case time complexity of setitem of the bottom level table is O(hash2(key2))
                        - All assignments and if statement are constant time.
        """
        del self.organisers[str(mountain.difficulty_level), mountain.name]

    def edit_mountain(self, old: Mountain, new: Mountain):
        """
          Arg:
          - old: Mountain to be removed from the hash table
          - new: Mountain to be added to the hash table

          Explain:
            - Essentially, this function rewrites the detail (diff, length) of a mountain.
            Gets the mountain from hash table by comparing the keys; if it exists, remove it and update the new mountain
            based on their difficulty_level and name.
          Complexity:
          - Worst case: O(add_mountain)(worst) + O(remove_mountain)(worst)
                        - Since this function just call the add_mountain and remove_mountain to update the new mountain.

          - Best case: O(add_mountain)(best) + O(remove_mountain)(best)
                        - Since this function just call the add_mountain and remove_mountain to update the new mountain.
        """
        self.remove_mountain(old)
        self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int):
        """
          Arg:
          - diff: Difficulty of mountains. Given this, return all mountains with this difficulty as a list.

          Explain:
            - Get the mountains with difficulty = diff from self.organisers by calling the values() function;

          Complexity:
          - Worst case: O(DoubleKeyTable.values())(worst) = O(N*M)
                        - When key is none, where N is the number of items in the top level table
                        - and M is the (average) number of items in the bottom level table.
                        - All assignments, if statements, return statement are constant time.

          - Best case: O(DoubleKeyTable.values())(best) = O(hash1(key) * hash2(key) * N)
                        - when key is the first element of the first table, and that second position of the second
                          table is empty (best case for linear probing).
                        - N is the number of items in the table.
        """
        return self.organisers.values(str(diff))

    def group_by_difficulty(self):
        """
          Explain:
            - Return a list of lists sorted by difficulty. Each list contains the group of all mountains with the
            same difficulty; we also rely upon the fact that each group is also already sorted by length/order

          Complexity:
          - Worst case: O(DoubleKeyTable.keys())(worst) +  O(NlogN * comp(tuple)) +O(N)
                        - where N is the length of self.organisers.
                        - for loop - O(N), where N is the length of self.organisers.
                            - append, accessing mountain_lst - O(1)
                        - return statement - O(1)

          - Worst case: O(DoubleKeyTable.keys())(best) +  O(NlogN * comp(tuple)) +O(N)
                        - where N is the length of self.organisers.
                        - for loop - O(N), where N is the length of self.organisers.
                            - append, accessing mountain_lst - O(1)
                        - return statement - O(1)
        """
        diff_groups = []
        keys = mergesort(self.organisers.keys())
        for difficulty in keys:
            diff_groups.append(self.organisers.values(difficulty))
        return diff_groups
