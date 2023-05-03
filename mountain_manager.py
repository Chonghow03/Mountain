from algorithms.mergesort import mergesort
from mountain import Mountain
from mountain_organiser import MountainOrganiser


class MountainManager:

    def __init__(self) -> None:
        self.MM_lst = []

    def add_mountain(self, mountain: Mountain):
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
        for MM in range(len(self.MM_lst)):
            if mountain.difficulty_level == self.MM_lst[MM][0]:
                mountain_organiser = self.MM_lst[MM][1]
                mountain_organiser.add_mountains([mountain])
                return
        mountain_organiser = MountainOrganiser()
        mountain_organiser.add_mountains([mountain])
        self.MM_lst.append((mountain.difficulty_level,mountain_organiser))

    def remove_mountain(self, mountain: Mountain):
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
        for MM in range(len(self.MM_lst)):
            if mountain.difficulty_level == self.MM_lst[MM][0]:
                mountain_organiser = self.MM_lst[MM][1]
                mountain_organiser.mountain_lst.remove(mountain)
                if len(mountain_organiser.mountain_lst) == 0:
                    self.MM_lst.remove(self.MM_lst[MM])
                return
        raise KeyError()

    def edit_mountain(self, old: Mountain, new: Mountain):
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
        for MM in range(len(self.MM_lst)):
            for mountain in MM[1].mountain_lst:
                if mountain == old:
                    mountain = new
        raise KeyError()

    def mountains_with_difficulty(self, diff: int):
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
        for i in range(len(self.MM_lst)):
            if diff == self.MM_lst[i][0]:
                mountain_organiser = self.MM_lst[i][1]
                return mountain_organiser.mountain_lst
        return []

    def group_by_difficulty(self):
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
        MM_mountain = []
        self.MM_lst = mergesort(self.MM_lst)
        for MO in self.MM_lst:
            MM_mountain.append(MO[1].mountain_lst)
        return MM_mountain


