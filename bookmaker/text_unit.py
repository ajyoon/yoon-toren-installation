from blur.markov.nodes import Node


class TextUnit:
    """
    A unit of text with formatting.
    """
    def __init__(self, text, italicized=False, bold=False):
        """
        Args:
            text (str):
            italicized (bool):
            bold (bool):
        """
        if isinstance(text, Node):
            self.text = text.name
        else:
            self.text = text
        self.italic = italicized
        self.bold = bold
