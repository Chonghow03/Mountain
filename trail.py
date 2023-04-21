from __future__ import annotations
from dataclasses import dataclass

import mountain
from data_structures.linked_stack import LinkedStack
from data_structures.stack_adt import Stack
from mountain import Mountain

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

    # The difficult part in this is TrailSplit.
    # TrailSplit has a path_follow, which we need to return to when we're done with the current path.
    # However, we can go into nested TrailSplits, so we need to keep track of all the paths we need to return to.
    # We can use a stack for this.
    # When we enter a TrailSplit, we push the path_follow onto the stack.
    # When we exit a TrailSplit, we pop the path_follow from the stack.
    # When the stack is empty, we're done with the trail.
    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""

        path = self.store

        # when the path enters a TrailSplit, path_follow is pushed onto this stack ;
        # when the path ultimately exits, is assigned the value of path_follow pop().
        path_to_join = LinkedStack()

        while True:
            if path is None:
                # check if path_to_join is non-empty (exiting a TrailSplit)
                if path_to_join.is_empty() is False:
                    path = path_to_join.pop()
                else:
                    print(personality.mountains)
                    break

            if type(path) == TrailSeries:
                personality.add_mountain(path.mountain)
                path = path.following.store
            elif type(path) == TrailSplit:

                # register path_to_join
                path_to_join.push(path.path_follow.store)

                if personality.select_branch(path.path_top, path.path_bottom):
                    # go into top path
                    path = path.path_top.store
                else:
                    # go into bottom path
                    path = path.path_bottom.store
        return None

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        mountains = []

        path = self.store

        # the size of the following two stacks should differ by at most 1
        follow_paths = LinkedStack()
        bottom_paths = LinkedStack()

        while True:
            if path is None:
                # check if path_to_join is non-empty (exiting a TrailSplit)
                if follow_paths.is_empty() is False:
                    if len(follow_paths) == len(bottom_paths):
                        path = bottom_paths.pop()
                    else:
                        path = follow_paths.pop()
                else:
                    break

            if type(path) == TrailSeries:
                mountains.append(path.mountain)
                path = path.following.store
            elif type(path) == TrailSplit:

                # register path_to_join
                follow_paths.push(path.path_follow.store)

                # store bottom path
                bottom_paths.push(path.path_bottom.store)

                # go into top path
                path = path.path_top.store

        return mountains


    def length_k_paths(self, k) -> list[list[Mountain]]:  # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """

        all_paths = []
        current_path = []
        current_k = 0
        path = self.store
        follow_paths = LinkedStack()

        print('finding path for k = ', k)

        # walk until reach a split
        while True:
            if path is None:
                if follow_paths.is_empty() is False:
                    path = follow_paths.pop()
                else:
                    # if current_k == k:
                    return [current_path]
                    # return []

            if type(path) == TrailSeries:
                current_path.append(path.mountain)
                current_k += 1
                path = path.following.store
            elif type(path) == TrailSplit:
                follow_paths.push(path.path_follow.store)
                is_split = True
                break
        print(path.path_top)
        print(path.path_bottom)
        if is_split:

            pass
        else:
            all_top_paths = path.path_top.length_k_paths(k-current_k)
            all_bottom_paths = path.path_bottom.length_k_paths(k-current_k)

        if len(all_top_paths) > 0:
            for top_path in all_top_paths:
                print('top_path', top_path)
                print([]+[1,2,3])
                all_paths.append(current_path+top_path)
                # all_paths.append(current_path.extend(top_path))
                print('final path', all_paths)
        if len(all_bottom_paths) > 0:
            for bottom_path in all_bottom_paths:
                all_paths.append(current_path+bottom_path)

        print('returning all_paths', all_paths)
        return all_paths

