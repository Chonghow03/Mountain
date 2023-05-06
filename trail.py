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
        Explain:
        A split in the trail.
           ___path_top____
          /               \
        -<                 >-path_follow-
          \__path_bottom__/

       Class variable:
       - path-top, which is a Trail instance with a argument TrailStore
       - path_bottom, which is a Trail instance with a argument TrailStore
       - path_follow, which is a Trail instance with a argument TrailStore
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def __init__(self, path_top, path_bottom, path_follow):
        self.path_top = path_top
        self.path_bottom = path_bottom
        self.path_follow = path_follow

    def remove_branch(self) -> TrailStore:
        """
           Explain:
           - Removes the branch, should just leave the remaining following trail.

           Args:
           - None

           Raises:
           - None

           Returns:
           - result: A TrailStore of path follow

           Complexity:
           - Worst case: O(1), return statement
           - Best case: O(1), return statement
        """

        return self.path_follow.store


@dataclass
class TrailSeries:
    """
       Explain:
       - A mountain, followed by the rest of the trail
         --mountain--following--

       Class variable:
       -mountain, which is a Mountain instance that involve three arguments (String name, Integer difficult_level, Integer length).
       -following, which is a Trail instance with the argument TrailStore.
    """
    mountain: Mountain
    following: Trail

    def __init__(self, mountain, trail):
        self.mountain = mountain
        self.following = trail

    def remove_mountain(self) -> TrailStore:
        """
           Explain:
           - Removes the mountain at the beginning of this series.

           Args:
           - None

           Raises:
           - None

           Returns:
           - result: A TrailStore of following trail

           Complexity:
           - Worst case: O(1), return statement
           - Best case: O(1), return statement
        """
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """
           Explain:
           - Adds a mountain in series before the current one.

           Args:
           - mountain, which is a Mountain instance that involve three arguments (String name, Integer difficult_level, Integer length).

           Raises:
           - None

           Returns:
           - result: A TrailSeries instance with two arguments (mountain and Trail instance).

           Complexity:
           - Worst case: O(1), return statement
           - Best case: O(1), return statement
        """
        return TrailSeries(mountain, Trail(store=TrailSeries(self.mountain, self.following)))

    def add_empty_branch_before(self) -> TrailStore:
        """
           Explain:
           - Adds an empty branch, where the current trailstore is now the following path.

           Args:
           - None

           Raises:
           - None

           Returns:
           - result: A TrailSplit with three arguments (path_top, path_bottom, path_follow)
           - Three arguments:
           -   path_top: Trail with TrailStore is None
           -   path_bottom: Trail with TrailStore is None
           -   path_follow: TrailSeries with self.mountain and self.following

           Complexity:
           - Worst case: O(1), return statement
           - Best case: O(1), return statement
        """
        return TrailSplit(Trail(None), Trail(None), Trail(TrailSeries(self.mountain, self.following)))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """
           Explain:
           - Adds a mountain after the current mountain, but before the following trail.

           Args:
           - mountain, which is a Mountain instance that involve three arguments (String name, Integer difficult_level, Integer length).

           Raises:
           - None

           Returns:
           - result: A TrailSeries with self.mountain and following is a Trail instance.
           - The Trail instance with TrailStore is TrailSeries (mountain that provided and following is self.following)

           Complexity:
           - Worst case: O(1), return statement
           - Best case: O(1), return statement
        """
        return TrailSeries(self.mountain, Trail(store=TrailSeries(mountain, self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """
           Explain:
           - Adds an empty branch after the current mountain, but before the following trail."

           Args:
           - None

           Raises:
           - None

           Returns:
           - result: A TrailSeries with self.mountain and following is a Trail instance.
           - The Trail instance with TrailStore is TrailSplit.
           - The TrailSplit with three arguments:
           -   path_top is Trail with TrailStore is None.
           -   path_bottom is Trail with TrailStore is None.
           -   path_follow is self.following.

           Complexity:
           - Worst case: O(1), return statement
           - Best case: O(1), return statement
        """
        return TrailSeries(self.mountain, Trail(TrailSplit(Trail(None), Trail(None), self.following)))


TrailStore = Union[TrailSplit, TrailSeries, None]


@dataclass
class Trail:
    """
       Class variable:
       - store: TrailStore is the union of TrailSplit, TrailSeries and None.

    """
    store: TrailStore = None

    def __init__(self, store):
        self.store = store

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """
           Explain:
           - Adds a mountain before everything currently in the trail.

           Args:
           - mountain, which is a Mountain instance that involve three arguments (String name, Integer difficult_level, Integer length).

           Raises:
           - None

           Returns:
           - result: A Trail instance with TrailStore is TrailSeries.
           - TrailSeries with two arguements mountain that provided, and following is Trail instance with TrailStore is None.

           Complexity:
           - Worst case: O(1), return statement
           - Best case: O(1), return statement
        """
        return Trail(TrailSeries(mountain, Trail(None)))

    def add_empty_branch_before(self) -> Trail:
        """
           Explain:
           - Adds an empty branch before everything currently in the trail.

           Args:
           - None

           Raises:
           - None

           Returns:
           - result: A Trail instance with TrailStore is TrailSplit.
           - The TrailSplit with three arguments,
           -   path_top is Trail with TrailStore is None.
           -   path_bottom is Trail with TrailStore is None.
           -   path_follow is Trail with TrailStore is None.

           Complexity:
           - Worst case: O(1), return statement
           - Best case: O(1), return statement
        """
        return Trail(TrailSplit(Trail(None), Trail(None), Trail(None)))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """
           Explain:
           -The function allows a predefined walker to follow a path, adding mountains according to its personality.

           - At each TrailSplit, we call the personality's select_branch function to determine which path to follow.
           - The personality is passed the top and bottom paths, and it returns True if we should follow the top path,
             or False if we should follow the bottom path.
           - Before we step into a TrailSplit, we push the path_follow onto a stack, so we can return to it later.
           - When we exit a TrailSplit, we pop from the stack to get the last path_follow.

           Args:
           - personality: walker with a predefined personality

           Complexity:
           The best case is simply O(1) when the trail is empty.
         
           - Best case: O(1) when the trail is empty
                        - create LinkedStack - O(1)
                        - check if trail is empty - O(1)
                        - return None - O(1)

            For worst case, since the trail selection is heavily dependent on the personality, we will be focusing on
            this aspect. We first notice that all operations are O(1), so the main concern is the number of iterations
            of the while loop i.e. length of branch.
            One such personality that will result in the worst case is a HardworkingWalker, which when encountering
            a branch, will always prioritize a TrailSplit branch to try to travel a longer 'distance'. We acknowledge the
            limitation that select_branch() does not have knowledge of the entire trail, so this will be the de facto
            worst case.

           - Worst case: O(M) when each encounter is a TrailSplit, and the personality is a HardworkingWalker,
           where M is the length of the longest path (that is, the number of TrailSplits in the longest path).
                        - create LinkedStack - O(1)

                        - do:
                        - check if trail is empty - O(1)
                            - set trail to follow_paths.pop() - O(1)
                        - check if trail is a TrailSplit - O(1)
                        - push path_follow onto stack - O(1)
                        - call personality.select_branch - O(1)
                        - step into TrailSplit - O(1)
                        - repeat while loop until follow_paths is empty- O(M)
        """

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
                    else trail.path_bottom.store  # select trail based on personality
        return None

    def collect_all_mountains(self) -> list[Mountain]:
        """
           Explain:
           - Returns a list of all mountains on the trail.

           Args:
           - None

           Raises:
           - None

           Returns:
           - result: list of all mountains created

           Complexity:
           - Worst case:
           - Best case:
        """

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
           Explain:
           - Returns a list of all paths of containing exactly k mountains.
             Paths are represented as lists of mountains.
             Paths are unique if they take a different branch, even if this results in the same set of mountains.

           Args:
           - k, which is an integer

           Raises:
           - None

           Returns:
           - result:

           Complexity:
           - Worst case:
           - Best case:
        """
        all_paths = []

        def traverse(trail, current_path, current_k, follow_stack=None):
            """
               Explain:
               -

               Args:
               - trail
               - current_path
               - current_k
               - follow_stack

               Raises:
               - None

               Returns:
               - result:

               Complexity:
               - Worst case:
               - Best case:
            """
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
