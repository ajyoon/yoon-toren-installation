import random

from blur import rand
import reportlab

from bookmaker import config


class Paragraph:
    """
    A styled list of ``TextUnit`` 's
    """
    def __init__(self, base_style, contents=None,
                 left_indent=0, right_indent=0, alignment='LEFT'):
        """
        Args:
            contents (list[TextUnit]): A list of ``TextUnit`` 's
                representing the content of the paragraph
            base_style (reportlab.lib.styles.ParagraphStyle):
            left_indent (int or float): left indentation value
                in 72-dpi units
            right_indent (int or float): right indentation value
                in 72-dpi units
            alignment (str): The alignment of the paragraph.
                Must be one of: ``'LEFT', 'CENTER', 'RIGHT', 'JUSTIFY'``
        """
        self.contents = contents if contents else []
        self.base_style = base_style
        self.left_indent = left_indent
        self.right_indent = right_indent
        self._alignment = None
        self.alignment = alignment

    @property
    def alignment(self):
        """
        str: The alignment of the paragraph.

        Must be one of: ``'LEFT', 'CENTER', 'RIGHT', 'JUSTIFY'``
        """
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        # Ensure legal values are passed.
        if value not in ['LEFT', 'CENTER', 'RIGHT', 'JUSTIFY']:
            raise ValueError("Paragraph.alignment must be either "
                             "'LEFT', 'CENTER', 'RIGHT', or 'JUSTIFY'")
        self._alignment = value

    def tweak_indent(self):
        """
        Correct any indentation errors.

        Prevents the left indentation line from crossing the right
        indentation line, prevents indentation lines from going outside
        of the page margins, and prevents the space between the indentation
        lines from being too small (not allowing enough room for legible
        paragraphs).

        Uses references to the following global constants
        located in ``config``:
        * config.PAGE_AREA_WIDTH
        * config.MIN_COLUMN_WIDTH

        Returns: None
        """

        # If left indent goes too far
        # (not leaving enough room for shared.MIN_COLUMN_WIDTH
        if self.left_indent > config.PAGE_AREA_WIDTH - config.MIN_COLUMN_WIDTH:
            self.left_indent = config.PAGE_AREA_WIDTH - config.MIN_COLUMN_WIDTH
        # If left indent goes outside of page
        elif self.left_indent < 0:
            self.left_indent = random.randint(0, 30)
            self.right_indent -= self.left_indent
        # If right indent is to the left of the left indent
        if (config.PAGE_AREA_WIDTH - self.right_indent <
                self.left_indent + config.MIN_COLUMN_WIDTH):
            self.right_indent = (config.PAGE_AREA_WIDTH - self.left_indent -
                                 config.MIN_COLUMN_WIDTH)
        # If right indent goes outside page
        elif self.right_indent < 0:
            self.right_indent = random.randint(0, 30)
            self.left_indent -= self.right_indent

    def pick_random_alignment(self):
        """
        Randomly pick a text alignment according to predefined weights.

        Returns: None
        """
        self.alignment = rand.weighted_choice(
                    [('LEFT', 70),
                     ('RIGHT', 5),
                     ('JUSTIFY', 15)
                     ])

    def add_text_unit(self, text_unit):
        """
        Add a ``TextUnit`` to ``self.contents``.

        Args:
            text_unit (TextUnit): The ``TextUnit`` to add to the paragraph.

        Returns: None
        """
        self.contents.append(text_unit)

    def to_reportlab_flowable(self):
        """
        Convert this object to a reportlab paragraph flowable.

        Returns:
            reportlab.platypus.Paragraph:
        """
        if self.alignment == 'LEFT':
            alignment_code = 0
        elif self.alignment == 'CENTER':
            alignment_code = 1
        elif self.alignment == 'RIGHT':
            alignment_code = 2
        elif self.alignment == 'JUSTIFY':
            alignment_code = 4
        else:
            raise ValueError

        # Assemble the paragraph string based on self.contents,
        # adding bold & italic runs where called for
        paragraph_string = ''
        for element in self.contents:
            run_text = element.text
            # new_run = new_line.add_run(element.text)
            if element.bold and not element.italic:
                run_text = '<b>' + run_text + '</b>'
            elif element.italic and not element.bold:
                run_text = '<i>' + run_text + '</i>'
            elif element.italic and element.bold:
                run_text = '<i><b>' + run_text + '</b></i>'
            if element.text == '\n':
                run_text = '<br/>'
            paragraph_string += run_text

        # Build the paragraph style to pass to the paragraph object
        style = reportlab.lib.styles.ParagraphStyle(
                name='modified paragraph style', parent=self.base_style,
                leftIndent=self.left_indent, rightIndent=self.right_indent,
                alignment=alignment_code)
        # Create the paragraph object and sent it to flowable_list
        return reportlab.platypus.Paragraph(paragraph_string, style)
