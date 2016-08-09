"""Custom Node subclasses"""

from blur.markov import nodes
from blur import soft


class BlankLine(nodes.Node):
    """A blank line with no value."""
    pass


class SoftFloatNode(nodes.Node):
    """
    A Node whose value is a representation of a SoftFloat
    """
    def __init__(self, weights, self_destruct=False):
        """
        Args:
            weights (list): Weights for a SoftFloat
            self_destruct (bool): whether this note deletes itself after
                being picked by a graph
        """
        nodes.Node.__init__(self, soft.SoftFloat(weights), self_destruct)

    def get_value(self):
        """
        Get a value of the SoftFloat

        Returns: float
        """
        return self.name.get()
