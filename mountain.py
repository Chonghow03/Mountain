from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Mountain:
    """
        Class variable:
        - String name
        - Integer difficulty_level
        - Integer length
    """

    name: str
    difficulty_level: int
    length: int

    def __lt__(self, other):
        """
            Explain:
            -

            Args:
            - other

            return:
            - Boolean

            Complexity:
            - Worst Case: O(1), all comparisons and return statement are constant time.

            - Best Case: O(1), all comparisons and return statement are constant time.
        """
        if self.length == other.length:
            return self.name < other.name
        else:
            return self.length < other.length

    def __gt__(self, other):
        """
            Explain:
            - If self length is equal to other length, we then compare name.
            - If self name is larger than other name, then return True otherwise return False.
            - If self length is not equal to other length, we then compare length.
            - If self length is larger than other length, then return True otherwise return False.

            Args:
            - other

            return:
            - Boolean

            Complexity:
            - Worst Case: O(1), all comparisons and return statement are constant time.

            - Best Case: O(1), all comparisons and return statement are constant time.
        """
        if self.length == other.length:
            return self.name > other.name
        else:
            return self.length > other.length

    def __le__(self, other):
        """
            Explain:
            - If self length is equal to other length, we then compare name.
            - If self name is smaller equal than other name, then return True otherwise return False.
            - If self length is not equal to other length, we then compare length.
            - If self length is smaller than other length, then return True otherwise return False.

            Args:
            - other

            return:
            - Boolean

            Complexity:
            - Worst Case: O(1), all comparisons and return statement are constant time.

            - Best Case: O(1), all comparisons and return statement are constant time.
        """
        if self.length == other.length:
            return self.name <= other.name
        else:
            return self.length < other.length

    def __ge__(self, other):
        """
            Explain:
            - If self length is equal to other length, we then compare name.
            - If self name is greater equal than other name, then return True otherwise return False.
            - If self length is not equal to other length, we then compare length.
            - If self length is greater than other length, then return True otherwise return False.

            Args:
            - other

            return:
            - Boolean

            Complexity:
            - Worst Case: O(1), all comparisons and return statement are constant time.

            - Best Case: O(1), all comparisons and return statement are constant time.
        """
        if self.length == other.length:
            return self.name >= other.name
        else:
            return self.length > other.length
