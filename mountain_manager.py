from mountain import Mountain
from mountain_organiser import MountainOrganiser


class MountainManager:

    def __init__(self) -> None:
        self.MM_lst = []

    def add_mountain(self, mountain: Mountain):
        for i in range(len(self.MM_lst)):
            if mountain.difficulty_level == self.MM_lst[i][0]:
                mountain_organiser = self.MM_lst[i][1]
                mountain_organiser.add_mountains([mountain])
                return
        mountain_organiser = MountainOrganiser()
        mountain_organiser.add_mountains([mountain])
        self.MM_lst.append((mountain.difficulty_level,mountain_organiser))

    def remove_mountain(self, mountain: Mountain):
        for i in range(len(self.MM_lst)):
            if mountain.difficulty_level == self.MM_lst[i][0]:
                mountain_organiser = self.MM_lst[i][1]
                mountain_organiser.mountain_lst.remove(mountain)
                return
        raise KeyError()

    def edit_mountain(self, old: Mountain, new: Mountain):
        raise NotImplementedError()

    def mountains_with_difficulty(self, diff: int):
        for i in range(len(self.MM_lst)):
            if diff == self.MM_lst[i][0]:
                mountain_organiser = self.MM_lst[i][1]
                return mountain_organiser.mountain_lst
        return []

    def group_by_difficulty(self):
        raise NotImplementedError()
