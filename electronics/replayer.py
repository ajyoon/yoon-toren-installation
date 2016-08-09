import numpy
from wavefile import WaveReader, Format
import time
import os
import random

from blur import rand

from electronics.amplitude import Amplitude
from electronics import config
from electronics.weighted_rand_utils import weighted_choice_preferring_later


def add_random_replayer(replayer_list, data_paths):
    """

    Args:
        replayer_list (list):
        data_paths (list):

    Returns: None
    """
    # TODO: Document me!
    #
    # Only allow playback of sounds at least 5 seconds old
    filtered_data_paths = []
    for path in data_paths:
        file_creation_time = int(os.path.basename(path)[:-6])
        age = int(time.time()) - file_creation_time
        if age > 5:
            filtered_data_paths.append(path)
    if filtered_data_paths:
        replayer_list.append(
                Replayer(weighted_choice_preferring_later(filtered_data_paths)))
        print('Adding player.'
              'Total number of active players: {0}'.format(len(replayer_list)))


def remove_random_replayer(replayer_list):
    """
    Args:
        replayer_list (list):

    Returns: None
    """
    # TODO: Document me!
    if len(replayer_list):
        del replayer_list[random.randint(0, len(replayer_list) - 1)]
        print('Removing player.'
              'Total number of active players: {0}'.format(len(replayer_list)))


def manage_replayers(data_paths, replayer_list,
                     add_player_prob, remove_player_prob):
    """
    Manage a list of ``Replayer`` 's, sometimes adding and removing items.

    Args:
        data_paths (list[str]):
        replayer_list (list[str]):
        add_player_prob (float): probability between 0 and 1 to add a replayer
            to the replayer list
        remove_player_prob (float): probability between 0 and 1 to to add a
            replayer to the replayer list

    Returns:

    """
    if rand.prob_bool(add_player_prob):
        add_random_replayer(replayer_list, data_paths)
    if rand.prob_bool(remove_player_prob):
        remove_random_replayer(replayer_list)


class Replayer:
    def __init__(self, wav_file, start_pos=None):
        """
        Args:
            wav_file (str): File path
            start_pos (int): Starting chunk index
        """
        self.file_path = wav_file
        self.file = WaveReader(wav_file, config.SAMPLE_RATE,
                               config.NUM_CHANNELS, Format.WAV | Format.PCM_16)
        if start_pos is None:
            self.playback_pos = random.randint(0, self.file.frames)
        else:
            self.playback_pos = start_pos

        # Lower the amplitude so that older files (indicated in file name)
            # are softer
        # Time the file was created in seconds
        file_creation_time = int(os.path.basename(self.file_path)[:-6])
        age = int(time.time()) - file_creation_time
        adjusted_age = age / 200
        if adjusted_age == 0:
            adjusted_age = 0.0001
        amp = (1 / adjusted_age) * 0.9
        if amp > 0.3:
            amp = 0.3

        self.amplitude = Amplitude(amp)

    def get_chunk(self):
        """
        Returns: None
        """
        # TODO: Document me!
        self.file.seek(self.playback_pos)
        # TODO: Is this zeros bit necessary?
        chunk = numpy.zeros((config.NUM_CHANNELS, config.CHUNK_SIZE),
                            numpy.int16,
                            order='F')
        # chunk = next(self.file.read_iter(shared.CHUNK_SIZE))
        # chunk = self.data[self.playback_pos] * self.amplitude.value
        # Multiply by amplitude here?
        chunk = chunk * self.amplitude.value
        # print(chunk.shape)
        self.playback_pos += config.CHUNK_SIZE
        if self.playback_pos > self.file.frames:
            self.playback_pos = 0
        return chunk
