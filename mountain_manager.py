from algorithms.mergesort import mergesort
from data_structures.hash_table import LinearProbeTable
from double_key_table import DoubleKeyTable
from mountain import Mountain
from mountain_organiser import MountainOrganiser


class MountainManager:
    """
    MountainManager acts as a store for mountains, and provides methods to add, remove and edit mountains.

    Mountains are stored in a list of tuples, which contains MountainOrganisers sorted by difficulty level. The choice
    of data structure allows us to easily call mergesort on the list of tuples (at group_by_difficulty()),
    which sorts the MountainOrganisers by difficulty, thereby increasing the efficiency of the MountainManager.
   """

    def __init__(self) -> None:
        """
         Explain:
           - Initialise a list self.organisers, which stores a list of tuple ('difficulty', MountainOrganiser)

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
            - Get the MountainOrganiser from self.organisers by comparing tuple[0];
             if it exists, and add the mountain to it.
            - If the MountainOrganiser does not exist, create a new MountainOrganiser and add the mountain to it.

          Complexity:
          - Worst case: O(N), where N is the length of self.organisers. This occurs when the MountainOrganiser with
          the corresponding difficulty does not exist, and we have to create a new MountainOrganiser and
          add the mountain to it.
                    - The for loop is O(N), where N is the length of self.organisers.
                        - comparison statement - O(1)
                        - assignment statement - O(1)
                        - add_mountain() - O(1)
                    - create a new MountainOrganiser and add the mountain to it - O(1)
                    - append to self.organisers - O(1)

          - Best case: O(1), when the first MountainOrganiser in self.organisers has the same difficulty as the mountain
          to add.
                    - The for loop is O(1), since we only loop through the first element in self.organisers.
                        - comparison statement - O(1)
                        - assignment statement - O(1)
                        - add_mountain() - O(1)
                        - return statement - O(1)
        """
        self.organisers[str(mountain.difficulty_level), mountain.name] = mountain


    def remove_mountain(self, mountain: Mountain):
        """
          Arg:
          - mountain: Mountain to be removed from the MountainManager

          Explain:
           - Get the MountainOrganiser from self.organisers by comparing tuple[0]; if it exists, remove the mountain
              from it.

          Complexity:
          - Worst case: O(N), where N is the length of self.organisers. This occurs when the MountainOrganiser with
            the corresponding difficulty is at the end of self.organisers; and it has a length of 0 after deleting the
            mountain, requiring us to remove the MountainOrganiser.
                    - The for loop is O(N), where N is the length of self.organisers.
                        - comparison statement - O(1)
                        - assignment statement - O(1)
                        - remove() - O(1)
                        - check length of mo.mountain_lst - O(1)
                        - remove mo from self.organisers - O(1)
                        - return statement - O(1)
          - Best case: O(1), when the first MountainOrganiser in self.organisers has the same difficulty as the mountain.
                    - The for loop is O(1), since we only loop through the first element in self.organisers.
                        - comparison statement - O(1)
                        - assignment statement - O(1)
                        - remove - O(1)
                        - return statement - O(1)
        """
        del self.organisers[str(mountain.difficulty_level), mountain.name]

    def edit_mountain(self, old: Mountain, new: Mountain):
        """
          Arg:
          - old: Mountain to be removed from the MountainManager
          - new: Mountain to be added to the MountainManager

          Explain:
            - Essentially, this function rewrites the detail (diff, length) of a mountain.
            Gets the MountainOrganiser from self.organisers by comparing tuple[0]; if it exists, remove it and then
            add the new mountain to the MountainOrganiser.

          Complexity:
          - Worst case: O(N), where N is the length of self.organisers. This occurs when the MountainOrganiser with
            the corresponding difficulty is at the end of self.organisers.
                    - The for loop is O(N), where N is the length of self.organisers.
                        - comparison statement - O(1)
                        - remove() - O(1)
                        - append to mo.mountain_lst - O(1)

          - Best case: O(1), when the first MountainOrganiser contains the mountain to be edited.
                    - The for loop is O(1), since we only loop through the first element in self.organisers.
                        - comparison statement - O(1)
                        - remove() - O(1)
                        - append to mo.mountain_lst - O(1)
                        - return statement - O(1)
        """
        self.remove_mountain(old)
        self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int):
        """
          Arg:
          - diff: Difficulty of mountains. Given this, return all mountains with this difficulty as a list.

          Explain:
            - Get the MountainOrganiser with difficulty = diff from self.organisers by comparing tuple[0];
            if it exists, return the list mountain_lst from the MountainOrganiser.

          Complexity:
          - Worst case: O(N), where N is the length of self.organisers. This occurs when the MountainOrganiser with
            the corresponding difficulty is at the end of self.organisers/ does not exist.
                    - The for loop is O(N), where N is the length of self.organisers.
                        - comparison statement - O(1)
                    - return statement - O(1)

          - Best case: O(1), when the first MountainOrganiser is the one with the corresponding difficulty.
                    - The for loop is O(1), since we only loop through the first element in self.organisers.
                        - comparison statement - O(1)
                        - return statement - O(1)
        """
        return self.organisers.values(str(diff))

    def group_by_difficulty(self):
        """
          Explain:
            - Return a list of lists sorted by difficulty. Each list contains the group of all mountains with the
            same difficulty; we also rely upon the fact that each group is also already sorted by length/order by
            MountainOrganiser.

          Complexity: O(NlogN * comp(tuple))
                    - mergesort() - O(NlogN * comp(tuple)), where N is the length of self.organisers.
                    - for loop - O(N), where N is the length of self.organisers.
                        - append, accessing mountain_lst - O(1)
                    - return statement - O(1)

                    overall: O(NlogN * comp(tuple))
        """
        diff_groups = []
        keys = mergesort(self.organisers.keys())
        for key in keys:
            diff_groups.append(self.organisers.values(key))

        return diff_groups


