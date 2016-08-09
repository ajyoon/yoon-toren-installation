#!/usr/bin/env python
"""Utility functions for easier interfacing with reportlab."""

import os

from bookmaker import config


def register_font_family(font_name='Crimson Text'):
    """
    Register a font family with the reportlab environment.

    Args:
        font_name (str): Name of the font family to register.
            Currently only ``'Crimson Text'`` is supported.

    Returns: None
    """
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase import ttfonts
    font_folder = os.path.join(config.RESOURCES_DIR, 'fonts')
    if font_name == 'Cormorant Garamond':
        # Font file paths
        normal = os.path.join(
                font_folder, 'CormorantGaramond-Regular.ttf')
        bold = os.path.join(
                font_folder, 'CormorantGaramond-Semibold.ttf')
        italic = os.path.join(
                font_folder, 'CormorantGaramond-Italic.ttf')
        bold_italic = os.path.join(
                font_folder, 'CormorantGaramond-SemiboldItalic.ttf')
        # Register with reportlab
        pdfmetrics.registerFont(
                ttfonts.TTFont('Cormorant Garamond', normal))
        pdfmetrics.registerFont(
                ttfonts.TTFont('Cormorant Garamond-Bold', bold))
        pdfmetrics.registerFont(
                ttfonts.TTFont('Cormorant Garamond-Italic', italic))
        pdfmetrics.registerFont(
                ttfonts.TTFont('Cormorant Garamond-BoldItalic', bold_italic))
        # Register font family
        pdfmetrics.registerFontFamily(
                'Cormorant Garamond',
                'Cormorant Garamond',
                'Cormorant Garamond-Bold',
                'Cormorant Garamond-Italic',
                'Cormorant Garamond-BoldItalic')
    else:
        raise ValueError('Font {0} is not available'.format(font_name))
