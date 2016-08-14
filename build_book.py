#!/usr/bin/env python

import time
import os
import sys
import random
import subprocess

from blur.markov import graph

from bookmaker import config, document_builder


# Start the clock
clock_start_time = time.time()

# Set up the document #########################################################
part_name = 'speaker'
# Set up text material paths relative to config.RESOURCES_DIR
source_dir = os.path.join(config.RESOURCES_DIR, 'Text Material')
source_1 = os.path.join(source_dir, 'source_1.txt')
source_2 = os.path.join(source_dir, 'source_2.txt')

source_list = [source_1, source_2]

word_distance_weights = {-50: 5, -15: 20, -7: 5,
                         1: 750, 2: 40, 3: 20, 4: 10, 5: 10,
                         6: 15, 7: 10, 8: 10, 9: 8, 10: 5,
                         11: 2, 12: 2, 13: 5, 14: 5, 15: 60}

# Build the document ##########################################################
graph_1 = graph.Graph.from_file(source_1, merge_same_words=True)
graph_2 = graph.Graph.from_file(source_2, merge_same_words=True)
part_scribe = document_builder.DocumentBuilder(
        [graph_1, graph_2],
        font_size=config.FONT_SIZE,
        font_name=config.FONT_NAME)

# Append a random number to the filename if the name is taken already
book_filename = '{0}.pdf'.format(part_name)
book_path = os.path.join(config.OUTPUT_DIR, book_filename)
while os.path.exists(book_path):
    random_file_index = str(random.randint(0, 100000))
    book_filename = '{0}_{1}.pdf'.format(part_name, random_file_index)
    book_path = os.path.join(config.OUTPUT_DIR, book_filename)

# Generate document contents
part_scribe.populate_item_list(config.WORD_COUNT)

# Render the book to pdf
part_scribe.render(book_path)

# Print time elapsed
time_elapsed = divmod(time.time() - clock_start_time, 60)
print('New book built in {0} minutes and {1} seconds.\n'
      'File is located in {2}'.format(
          int(time_elapsed[0]), int(time_elapsed[1]), book_path))

if config.OPEN_WHEN_FINISHED:
    if sys.platform == 'linux' or sys.platform == 'linux2':
        command = 'xdg-open'
    elif sys.platform == 'darwin':
        command = 'open'
    elif sys.platform == 'win32':
        command = 'start'
    else:
        print('Could not automatically open the document for OS platform ' +
              sys.platform)
        command = None
    if command:
        subprocess.call([command, book_path])
