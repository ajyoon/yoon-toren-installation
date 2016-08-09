"""Config values for easy changing."""

import os

import pyaudio

# These device indices may need to be modified depending on the
# audio configuration of your machine. To view a list of available device
# device indices, go to run_electronics.py, set DEBUG=True, and run the script.
INPUT_DEVICE_INDEX = 3
OUTPUT_DEVICE_INDEX = 3

NUM_CHANNELS = 1
SAMPLE_RATE = 44100
CHUNK_SIZE = 1024
# TODO: changing STREAM_FORMAT alone is not enough to actually change the
#     format, implement the ability to do this.
STREAM_FORMAT = pyaudio.paInt16

TEMP_DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'temp_data/')
