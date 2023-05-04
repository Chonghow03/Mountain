import copy

from algorithms.mergesort import mergesort
from mountain import Mountain
from mountain_organiser import MountainOrganiser


class MountainManager:

    def __init__(self) -> None:
        self.organisers = []  # stores a list of tuple ('difficulty', MountainOrganiser)

    def add_mountain(self, mountain: Mountain):
        for organiser_tuple in self.organisers:
            if mountain.difficulty_level == organiser_tuple[0]:
                mo = organiser_tuple[1]
                # mo.add_mountains(copy.deepcopy([mountain]))
                mo.add_mountains([mountain])
                return
        mo = MountainOrganiser()
        mo.add_mountains([mountain])
        self.organisers.append((mountain.difficulty_level, mo))

    def remove_mountain(self, mountain: Mountain):
        for organiser_tuple in self.organisers:
            if mountain.difficulty_level == organiser_tuple[0]:
                mo = organiser_tuple[1]
                mo.mountain_lst.remove(mountain)
                if len(mo.mountain_lst) == 0:
                    self.organisers.remove(organiser_tuple)
                return
        raise KeyError()

    def edit_mountain(self, old: Mountain, new: Mountain):
        # for organiser_tuple in range(len(self.organisers)):
        #     for mountain in organiser_tuple[1].mountain_lst:
        #         if mountain == old:
        #             mountain = new
        for organiser_tuple in self.organisers:
            for mountain in organiser_tuple[1].mountain_lst:
                if mountain == old:
                    organiser_tuple[1].mountain_lst.remove(mountain)
                    organiser_tuple[1].mountain_lst.append(new)
                    print('found')
                    return
                else:
                    print(mountain, '!=', old)
        print("Mountain not found")
        raise KeyError()

    def mountains_with_difficulty(self, diff: int):
        for organiser_tuple in self.organisers:
            if diff == organiser_tuple[0]:
                return organiser_tuple[1].mountain_lst
        return []  # if no mountains with that difficulty

    def group_by_difficulty(self):
        diff_groups = []
        self.organisers = mergesort(self.organisers)
        for organiser_tuple in self.organisers:
            diff_groups.append(organiser_tuple[1].mountain_lst)
        return diff_groups


