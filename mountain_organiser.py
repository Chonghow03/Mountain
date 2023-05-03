from __future__ import annotations

import copy

from algorithms.binary_search import binary_search
from algorithms.mergesort import mergesort
from mountain import Mountain

class MountainOrganiser:

    def __init__(self) -> None:
        self.mountain_lst = []

    def cur_position(self, mountain: Mountain) -> int:
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
        index = binary_search(self.mountain_lst,mountain)
        if self.mountain_lst[index] != mountain:
            raise KeyError()
        return index

    def add_mountains(self, mountains: list[Mountain]) -> None:
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
        self.mountain_lst += mountains
        self.mountain_lst = mergesort(self.mountain_lst)
