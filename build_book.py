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
text_folder = os.path.join(config.RESOURCES_DIR, 'Text Material')
source_1 = os.path.join(text_folder, 'source_1.txt')
source_2 = os.path.join(text_folder, 'source_2.txt')

source_list = [source_1, source_2]

relationship_weights = {-50: 5, -15: 20, -7: 5,
                        1: 750, 2: 40, 3: 20, 4: 10, 5: 10,
                        6: 15, 7: 10, 8: 10, 9: 8, 10: 5,
                        11: 2, 12: 2, 13: 5, 14: 5, 15: 60}

# Build the document ##########################################################
word_count = config.WORD_COUNT
graph_1 = graph.Graph.from_file(source_1, merge_same_words=True)
graph_2 = graph.Graph.from_file(source_2, merge_same_words=True)
part_scribe = document_builder.DocumentBuilder(
        [graph_1, graph_2],
        font_size=config.FONT_SIZE,
        font_name=config.FONT_NAME)
random_file_index = str(random.randint(0, 100000))
base_filename = "{0}_base_{1}.pdf".format(part_name,
                                          random_file_index)
part_base_pdf_path = os.path.join(config.OUTPUT_DIR,
                                  base_filename)

# Main document population
part_scribe.populate_item_list(word_count)

# Render the part to pdf
base_part = part_scribe.render(part_base_pdf_path)

# Print time elapsed
time_elapsed = divmod(time.time() - clock_start_time, 60)
print("New part built in " + str(int(time_elapsed[0])) +
      ' minutes and ' + str(int(time_elapsed[1])) + ' seconds\n' +
      'Located in ' + base_part)

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
        subprocess.call([command, base_part])
