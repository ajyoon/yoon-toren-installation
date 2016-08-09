"""Utility functions for weighted random operations."""

from blur import rand

def weighted_choice_preferring_later(select_list):
    """
    Randomly choose an item, picking higher index items.

    Args:
        select_list (list): A list of

    Returns:
        Any: Any one of the items in ``select_list``
    """
    weight_list = []
    for i in range(0, len(select_list)):
        weight_list.append((select_list[i], (i + 5) / 2))
    return rand.weighted_choice(weight_list)