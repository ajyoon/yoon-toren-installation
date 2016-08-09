import os
import time
import numpy

from wavefile import WaveWriter, Format

from electronics import config


class Recorder:

    def __init__(self):
        self.currently_recording = False
        self.file_path = self.build_file_path()
        self.file = WaveWriter(self.file_path,
                               config.SAMPLE_RATE,
                               config.NUM_CHANNELS,
                               Format.WAV | Format.PCM_16)

    def add_data(self, in_data):
        write_data = numpy.atleast_2d(numpy.fromstring(in_data, numpy.int16))
        self.file.write(write_data)

    def reset(self):
        self.__init__()

    @staticmethod
    def build_file_path():
        return os.path.join(config.TEMP_DATA_FOLDER,
                            '{0}.wav'.format(round(time.time()*100)))