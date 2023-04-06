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

    def __init__(self):
        self.myLinkedStack=LinkedStack(Stack(1000))

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        self.myLinkedStack.pop()

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def __init__(self):
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
        self.myLinkedstack.push(mountain)
        self.myLinkedstack.push(last_mountain)


    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        raise NotImplementedError()

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        raise NotImplementedError()

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        raise NotImplementedError()

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def __init__(self):
        self.myLinkedstack = LinkedStack(Stack(1000))

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        self.myLinkedstack.push(mountain)

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        self.myLinkedstack.push(None)

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        raise NotImplementedError()

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        raise NotImplementedError()

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        raise NotImplementedError()