"""Command line argument parser for the run_electronics script."""

import argparse

from electronics import config

parser = argparse.ArgumentParser(
    description='Yoon/Toren Installation 5/10/2016 - Audio Processing Script')
parser.add_argument('-d', '--debug',
                    dest='debug',
                    action='store_true',
                    help='Run in debug mode (more verbose console output)')
parser.add_argument('-i', '--input-device-index',
                    dest='input_device_index',
                    action='store',
                    type=int,
                    default=config.DEFAULT_INPUT_DEVICE_INDEX,
                    help='The index of the device to handle audio input. '
                         '(hint: run in debug mode to print a list of '
                         'available device indices. You can also edit the '
                         'default value of this in electronics/config.py)')
parser.add_argument('-o', '--output-device-index',
                    dest='output_device_index',
                    action='store',
                    type=int,
                    default=config.DEFAULT_OUTPUT_DEVICE_INDEX,
                    help='The index of the device to handle audio output. '
                         '(hint: run in debug mode to print a list of '
                         'available device indices. You can also edit the '
                         'default value of this in electronics/config.py)')
