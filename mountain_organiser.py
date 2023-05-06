from __future__ import annotations

from algorithms.binary_search import binary_search
from algorithms.mergesort import mergesort
from mountain import Mountain


class MountainOrganiser:
    """
      MountainOrganiser is a simple 1-dimensional data structure that stores mountains in a list. It maintains
        the order of the mountains in the list through mergesort.
     """

    def __init__(self) -> None:
        """
         Explain:
           - Initialise a list self.mountain_lst, which stores a list of Mountain objects

         Complexity:
         - Worst case: O(1), assignment is O(1) (constant time)
         - Best case: O(1), assignment is O(1) (constant time)
        """
        self.mountain_lst = []

    def cur_position(self, mountain: Mountain) -> int:
        """
           Explain:
           - Given a mountain, return the index (sorted position) of the mountain in self.mountain_lst

           Args:
           - mountain: Mountain that is currently being searched for

           Raises:
             - KeyError: If the mountain does not exist in self.mountain_lst

           Returns:
           - index: Index of the mountain in self.mountain_lst

           Complexity:
           - Worst case: O(logN), where N is the length of self.mountain_lst. This occurs when the mountain is
              located in the leftmost/rightmost, and we have to perform binary search on the entire list.
                    - binary_search() - O(logN)
                    - comparison statement - O(1)
                    - return statement - O(1)
           - Best case: O(1), when the mountain is located in the middle of the list, and we can return the index
                immediately.
                    - binary_search() - O(1)
                    - comparison statement - O(1)
                    - return statement - O(1)
        """
        index = binary_search(self.mountain_lst, mountain)
        if self.mountain_lst[index] != mountain:
            raise KeyError()
        return index

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
           Explain:
           - Given a list of mountains, add them to self.mountain_lst and sort the list using mergesort, maintaining
                the order of the mountains in the list.

           Args:
           - mountains: List of mountains to be added to self.mountain_lst

           Complexity: O(NlogN), where N is the length of self.mountain_lst. Best case and worst case are the same.
                - appending to self.mountain_lst - O(1)
                - mergesort() - O(NlogN)
        """
        self.mountain_lst += mountains
        self.mountain_lst = mergesort(self.mountain_lst)
