from __future__ import annotations
from dataclasses import dataclass

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
        self.path_top = Trail(None)
        self.path_bottom = Trail(None)
        self.path_follow = Trail(None)
        return


@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def __init__(self,mountain,following):
        self.myLinkedstack = LinkedStack(Stack(1000))
        self.copyLinkedstack = LinkedStack(Stack(len(self.myLinkedstack)))

    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series."""
        for count in range(len(self.myLinkedstack)):
            self.copyLinkedstack.push(self.myLinkedstack.pop())
        self.copyLinkedstack.pop()
        for count in range(len(self.copyLinkedstack)):
            self.myLinkedstack.push(self.copyLinkedstack.pop())



    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
        last_mountain = self.myLinkedstack.pop()
        self.myLinkedstack.push((mountain,None))
        self.myLinkedstack.push(last_mountain)
        return self.myLinkedstack

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        last_mountain = self.myLinkedstack.pop()
        self.myLinkedstack.push(TrailSplit(Trail(None),Trail(None),Trail(None)))
        self.myLinkedstack.push(last_mountain)
        return self.myLinkedstack
    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        return self.myLinkedstack.push((mountain,None))

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        return self.myLinkedstack.push(TrailSplit(Trail(None),Trail(None),Trail(None)))

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    # def __init__(self):
    #     self.myLinkedstack = LinkedStack()

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        TrailStore.push((TrailStore,mountain))
        return TrailStore

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        self.myLinkedstack.push(TrailSplit(Trail(None),Trail(None),Trail(None)))
        return self.trail_store


    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        pass

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

t=Trail(None)
t.add_mountain_before(Mountain("m",5,5))