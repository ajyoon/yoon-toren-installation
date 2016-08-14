import random

from blur import rand
import reportlab.lib.enums
import reportlab.lib.styles
import reportlab.pdfgen.canvas
import reportlab.platypus
import reportlab.rl_config
from reportlab.lib import units

from bookmaker import custom_nodes
from bookmaker import paragraph
from bookmaker import prebuilt_graphs
from bookmaker import reportlab_utils
from bookmaker import text_unit


class DocumentBuilder:
    """
    The class responsible for generating the book.
    """

    _PUNCTUATION_LIST = [',', '.', ':', '!', '?', '"', '\'', ';']

    def __init__(self, word_graphs,
                 font_size=11, font_name='Cormorant Garamond',
                 title=None, draw_header=True):
        """
        Args:
            word_graphs (list): a list of ``blur`` ``Graph``
                markov graphs indicating which words follow which.
            font_size (float or int): the font size to be used throughout.
            font_name (str): The name of the font family to use throughout.
                must be a value implemented by
                ``reportlab_utils.register_font_family``
            draw_header (bool):
            title (str): Title to appear in the header. This value is also
                used in generating the output file name
        """
        self.title = title

        self.word_graphs = word_graphs
        self.draw_header = draw_header
        self.item_list = []
        self.flowable_list = []

        # Initialize font from global FontName
        reportlab_utils.register_font_family(font_name)
        # Set up paragraph_style, passing in globals
        self.paragraph_style = reportlab.lib.styles.ParagraphStyle(
                'Default Style',
                fontSize=font_size,
                fontName=font_name)
        self.indenter_left = prebuilt_graphs.indenter()
        self.indenter_right = prebuilt_graphs.indenter()
        self.pause_or_write_network = prebuilt_graphs.text_pause_or_write()

    def populate_item_list(self, item_count):
        """
        Fill ``self.item_list`` with Node instances.

        Args:
            item_count (int): Number of items to create

        Returns: None
        """

        graph_weights = [(network, 1) for network in self.word_graphs]

        # Pick a random network to start on
        current_network = random.choice(self.word_graphs)

        # Main item population loop
        for i in range(item_count):
            # Determine if we should change networks (crude)
            if rand.prob_bool(0.01):
                old_network = current_network
                while current_network == old_network:
                    current_network = rand.weighted_choice(graph_weights)

            # Determine with self.pause_or_write_network whether to append a
            # blank line or a word to self.item_list
            if self.pause_or_write_network.pick().get_value() == 0:
                self.item_list.append(custom_nodes.BlankLine())
            else:
                new_node = current_network.pick()
                self.item_list.append(new_node)

    def render(self, output_file):
        """
        Render items in ``self.item_list`` to a PDF file.

        Args:
            output_file (str): Output file path

        Returns:
            str: Path to the newly built PDF file.
        """
        # TODO: Continue de-spaghettifying
        # Cycle through all nodes stored in self.item_list,
        # use them to fill the contents of self.flowable_list
        current_line = paragraph.Paragraph(self.paragraph_style)
        for current_item in self.item_list:
            # Find indentation and alignment
            current_line.left_indent += self.indenter_left.pick().get_value()
            current_line.right_indent += self.indenter_right.pick().get_value()
            current_line.tweak_indent()
            current_line.pick_random_alignment()

            if isinstance(current_item, custom_nodes.BlankLine):
                if current_line.contents is not None:
                    # Send current_line contents to a new line
                    self.flowable_list.append(
                            current_line.to_reportlab_flowable())
                    current_line = paragraph.Paragraph(self.paragraph_style)
                self.flowable_list.append(
                        reportlab.platypus.Spacer(
                                16, self.paragraph_style.fontSize))
            elif current_item.name in DocumentBuilder._PUNCTUATION_LIST:
                # Punctuation marks
                temp_string = current_item.name
                current_line.add_text_unit(text_unit.TextUnit(temp_string))
            else:
                # Words
                temp_string = current_item.name
                if current_line.contents:
                    # If the current line already has contents, add a space
                    # before this word
                    temp_string = " " + temp_string
                current_line.add_text_unit(text_unit.TextUnit(temp_string))

        # After end of document, add what's left to the document
        if current_line.contents:
            self.flowable_list.append(current_line.to_reportlab_flowable())

        # Save the doc to an output pdf file ##################################
        def _build_header_canvas(canvas, doc):
            """
            Draw the document header.

            Local function to be passed later to output_doc.build().
            Reportlab automatically passes args when called.
            """
            # The header function to be passed later to output_doc.build()
            # Set up positions
            header_y_position = (11 * units.inch) - 45
            page_number = doc.page
            if page_number % 2 == 0:
                # Left-hand page
                page_number_x_position = 60
            else:
                # Right-hand page
                page_number_x_position = (8.5 * units.inch) - 60
            canvas.saveState()
            canvas.setFont(self.paragraph_style.fontName,
                           self.paragraph_style.fontSize)
            if self.title:
                canvas.drawCentredString((8.5 * units.inch) / 2,
                                         header_y_position,
                                         self.title)
            canvas.drawString(page_number_x_position, header_y_position,
                              str(page_number))
            canvas.restoreState()

        output_doc = reportlab.platypus.SimpleDocTemplate(output_file)
        output_doc.pagesize = (8.5 * units.inch, 11 * units.inch)
        if self.draw_header:
            output_doc.build(self.flowable_list,
                             onFirstPage=_build_header_canvas,
                             onLaterPages=_build_header_canvas)
        else:
            output_doc.build(self.flowable_list)

        # Return path to the final built pdf
        return output_file
