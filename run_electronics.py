#!/usr/bin/env python

import numpy
import pyaudio
import time
import signal
import sys

from pprint import pprint

from electronics import cli_argparser
from electronics import replayer
from electronics import amplitude
from electronics.amp_threshold_tracker import AmpThresholdTracker
from electronics.recorder import Recorder
from electronics.oscillator import Oscillator
from electronics import config
from electronics.frequency_map import frequency_map

# Make sure we're running the right version of Python
if sys.version_info[0] != 3:
    print('This program must be run on Python 3, make sure Python 3 \n'
          'is on your environment path. see the Python website for help.')
    sys.exit(1)

# Get command line arguments ##################################################

cli_args = cli_argparser.parser.parse_args()
DEBUG = cli_args.debug
INPUT_DEVICE_INDEX = cli_args.input_device_index
OUTPUT_DEVICE_INDEX = cli_args.output_device_index

# Set up script state #########################################################

threshold_tracker = AmpThresholdTracker()

pitches = [
    frequency_map[6] / 32,
    frequency_map[6] / 16,
    frequency_map[6] / 4,
    frequency_map[6] / 2,
    frequency_map[5],
    frequency_map[8],
    frequency_map[0] * 2,
    frequency_map[1] * 2,
    frequency_map[10] * 2
    ]

oscillators = []
for frequency in pitches:
    oscillators.append(
        Oscillator(
            frequency,
            amplitude.Amplitude(
                drift_target_weights=[
                    (-1, 1), (0.02, 6), (0.2, 5), (0.3, 1), (0.4, 0)
                    ],
                change_rate_weights=[
                    (0.0000001, 12000),
                    (0.00001, 100),
                    (0.0001, 10)
                    ]
            )
        )
    )

# List of paths to wav files stored on disk
data_paths = []
replayers = []
recorder = Recorder()

add_player_prob = 0.002
remove_player_prob = 0.007
add_player_weights = [(180, 10), (300, 2), (500, 1)]
remove_player_weights = [(75, 2), (150, 10), (200, 3), (250, 1)]


def main_callback(in_data, frame_count, time_info, status):
    """
    The main callback function used by pyaudio during audio I/O streaming.
    """
    subchunks = []
    for osc in oscillators:
        osc.amplitude.step_amp()
        subchunk = osc.get_samples(config.CHUNK_SIZE)
        if subchunk is not None:
            subchunks.append(subchunk)

    replayer.manage_replayers(data_paths, replayers,
                              add_player_prob, remove_player_prob)
    for player in replayers:
        subchunks.append(player.get_chunk())

    new_chunk = sum(subchunks)

    in_amplitude = amplitude.find_amplitude(in_data)
    if threshold_tracker.crosses_threshold(in_amplitude):
        # If the input amplitude goes over the threshold
        if not recorder.currently_recording:
            recorder.currently_recording = True
            print('Enabling Recording due to input amplitude of {0}'.format(
                    in_amplitude))
        threshold_tracker.last_threshold_cross_time = time.time()
    else:
        # If it's been AmpThresholdTracker.below_threshold_cutoff_dur since
        # in_data has crossed the threshold, turn off the recorder
        if (time.time() > (threshold_tracker.last_threshold_cross_time +
                threshold_tracker.below_threshold_cutoff_dur) and
                recorder.currently_recording):
            recorder.reset()
            data_paths.append(recorder.file_path)
            print('Disabling Recording')

    if recorder.currently_recording:
        recorder.add_data(in_data)

    # Play sound
    return new_chunk.astype(numpy.int16).tostring(), pyaudio.paContinue

# Main script execution #######################################################

# Print program introduction and instructions for how to exit
print('Yoon/Toren Installation 5/10/2016 - Audio Processing Script\n'
      'To exit, press Control-C.')

# Launch PyAudio instance
pa_host = pyaudio.PyAudio()
main_stream = pyaudio.Stream(pa_host,
                             rate=config.SAMPLE_RATE,
                             channels=config.NUM_CHANNELS,
                             format=config.STREAM_FORMAT,
                             input=True,
                             output=True,
                             input_device_index=INPUT_DEVICE_INDEX,
                             output_device_index=OUTPUT_DEVICE_INDEX,
                             frames_per_buffer=config.CHUNK_SIZE,
                             stream_callback=main_callback)
main_stream.start_stream()

# Print device information for all available devices
if DEBUG:
    print('Available device information =================================')
    try:
        x = 0
        while True:
            pprint(pa_host.get_device_info_by_host_api_device_index(0, x))
            x += 1
    except IOError:
        pass


# Main loop ###################################################################

def quit_signal_handler(signal, frame):
    """Handler for quitting on keyboard interrupt"""
    # TODO: Fade out instead of just cutting off
    print('\n\nGoodbye...')
    main_stream.close()
    pa_host.terminate()
    sys.exit(0)

# Register keyboard interrupt signal handler
signal.signal(signal.SIGINT, quit_signal_handler)

while True:
    time.sleep(config.CHUNK_SIZE / config.SAMPLE_RATE)
