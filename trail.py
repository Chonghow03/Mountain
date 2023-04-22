from __future__ import annotations
from dataclasses import dataclass

from data_structures.linked_stack import LinkedStack
from mountain import Mountain
import copy

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality


@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def __init__(self, path_top, path_bottom, path_follow):
        self.path_top = path_top
        self.path_bottom = path_bottom
        self.path_follow = path_follow

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        return self.path_follow.store


@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def __init__(self, mountain, trail):
        self.mountain = mountain
        self.following = trail

    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series."""
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
        return TrailSeries(mountain, Trail(store=TrailSeries(self.mountain, self.following)))

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        return TrailSplit(Trail(None), Trail(None), Trail(TrailSeries(self.mountain, self.following)))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        return TrailSeries(self.mountain, Trail(store=TrailSeries(mountain, self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        return TrailSeries(self.mountain, Trail(TrailSplit(Trail(None), Trail(None), self.following)))


TrailStore = Union[TrailSplit, TrailSeries, None]


@dataclass
class Trail:
    store: TrailStore = None

    def __init__(self, store):
        self.store = store

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        return Trail(TrailSeries(mountain, Trail(None)))

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        return Trail(TrailSplit(Trail(None), Trail(None), Trail(None)))

    # TrailSplit has a path_follow, which we need to return to when we're done with the current path.
    # However, we can go into nested TrailSplits, so we need to keep track of all the paths we need to return to.
    # When we enter a TrailSplit, we push the path_follow onto a stack.
    # When we exit a TrailSplit, we get path_follow by popping from the stack.
    # When the stack is empty, we're done with the trail.
    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        trail = self.store
        follow_paths = LinkedStack()

        while True:
            if trail is None:
                if follow_paths.is_empty():  # if
                    break
                trail = follow_paths.pop()  # else
            if isinstance(trail, TrailSeries):
                personality.add_mountain(trail.mountain)
                trail = trail.following.store
            elif isinstance(trail, TrailSplit):
                follow_paths.push(trail.path_follow.store)
                trail = trail.path_top.store if personality.select_branch(trail.path_top, trail.path_bottom) \
                    else trail.path_bottom.store   # select trail based on personality
        return None

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        # mountains = []
        #
        # path = self.store
        #
        # # the size of the following two stacks should always be same, and differ by at most 1 when traversing
        # follow_paths = LinkedStack()
        # bottom_paths = LinkedStack()
        #
        # while True:
        #     if path is None:
        #         # check if path_to_join is non-empty (exiting a TrailSplit)
        #         if follow_paths.is_empty():
        #             break
        #         else:
        #             if len(follow_paths) == len(bottom_paths):  # nav bottom before we exit
        #                 path = bottom_paths.pop()
        #             else:
        #                 path = follow_paths.pop()
        #
        #     if type(path) == TrailSeries:
        #         mountains.append(path.mountain)
        #         path = path.following.store
        #     elif type(path) == TrailSplit:
        #
        #         # register path_to_join
        #         follow_paths.push(path.path_follow.store)
        #
        #         # store bottom path
        #         bottom_paths.push(path.path_bottom.store)
        #
        #         # go into top path
        #         path = path.path_top.store
        #
        # return mountains

        import copy
        all_mountains = []

        def traverse(trail, current_path, current_k, follow_stack=None):
            follow_stack_copy = copy.deepcopy(follow_stack)
            current_path_copy = copy.deepcopy(current_path)
            if trail is None:
                if not follow_stack_copy.is_empty():
                    traverse(follow_stack_copy.pop(), current_path_copy, current_k, follow_stack_copy)
                return  # not necessary, but makes it clear that this is the end of the path
            elif isinstance(trail, TrailSeries):
                # this code below differs all_mountains() from length_k_paths()
                if trail.mountain not in all_mountains:
                    all_mountains.append(trail.mountain)

                current_path_copy.append(trail.mountain)
                traverse(trail.following.store, current_path_copy, current_k + 1, follow_stack_copy)
            elif isinstance(trail, TrailSplit):
                follow_stack_copy.push(trail.path_follow.store)
                traverse(trail.path_top.store, current_path_copy, current_k, follow_stack_copy)
                traverse(trail.path_bottom.store, current_path_copy, current_k, follow_stack_copy)

        traverse(self.store, [], 0, LinkedStack())
        return all_mountains


    def length_k_paths(self, k) -> list[list[Mountain]]:  # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        all_paths = []

        def traverse(trail, current_path, current_k, follow_stack=None):
            follow_stack_copy = copy.deepcopy(follow_stack)
            current_path_copy = copy.deepcopy(current_path)
            if trail is None:
                if not follow_stack_copy.is_empty():
                    traverse(follow_stack_copy.pop(), current_path_copy, current_k, follow_stack_copy)
                if current_k == k:
                    all_paths.append(current_path_copy)
                return  # not necessary, but makes it clear that this is the end of the path
            elif isinstance(trail, TrailSeries):
                current_path_copy.append(trail.mountain)
                traverse(trail.following.store, current_path_copy, current_k + 1, follow_stack_copy)
            elif isinstance(trail, TrailSplit):
                follow_stack_copy.push(trail.path_follow.store)
                traverse(trail.path_top.store, current_path_copy, current_k, follow_stack_copy)
                traverse(trail.path_bottom.store, current_path_copy, current_k, follow_stack_copy)

        traverse(self.store, [], 0, LinkedStack())
        return all_paths



