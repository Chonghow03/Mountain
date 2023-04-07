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

    def __init__(self,path_top,path_bottom,path_follow):
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
        return TrailSeries(mountain,Trail(store=TrailSeries(self.mountain,self.following)))

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        return TrailSplit(Trail(None),Trail(None),Trail(TrailSeries(self.mountain,self.following)))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        return TrailSeries(self.mountain,Trail(store=TrailSeries(mountain,self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        return TrailSeries(self.mountain,Trail(TrailSplit(Trail(None),Trail(None),self.following)))

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def __init__(self,store):
        self.store = store

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        return Trail(TrailSeries(mountain,Trail(None)))


    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        return Trail(TrailSplit(Trail(None),Trail(None),Trail(None)))


    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        store = self.store
        while store != None:
            if type(store) == TrailSeries:
                store = store.following
                personality.add_mountain(store.mountain)
            elif type(store) == TrailSplit:
                if personality.select_branch(store.path_top,store.path_bottom):
                    # todo merge top path with following path
                    store = TrailSeries(None, store.path_top)
                else:
                    store = store.path_bottom


    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        pass

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        pass

