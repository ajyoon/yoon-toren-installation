#!/usr/bin/env python
"""Configuration constants for easy tweaking."""


import os

from reportlab.lib import units

OUTPUT_DIR = os.path.realpath(
    os.path.join(os.path.dirname(__file__), 'output'))
RESOURCES_DIR = os.path.realpath(
    os.path.join(os.path.dirname(__file__), 'resources'))

LEFT_MARGIN = 1 * units.inch
RIGHT_MARGIN = 1 * units.inch

# 8.5 Inch document, 1 inch margins on left & right
# gives 6.5 inches of working space
PAGE_AREA_WIDTH = 6.5 * units.inch
MIN_COLUMN_WIDTH = 1.25 * units.inch

FONT_NAME = 'Cormorant Garamond'
FONT_SIZE = 11  # 72-dpi points

WORD_COUNT = 8000

OPEN_WHEN_FINISHED = True
