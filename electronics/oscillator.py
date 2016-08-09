import numpy
from electronics.amplitude import Amplitude
from electronics.config import SAMPLE_RATE


class Oscillator:
    """
    A sine wave oscillator.
    """
    def __init__(self, frequency,
                 amplitude=None,
                 start_mode='ON'):
        """
        Args:
            frequency (float):
            sample_rate (int):
            amplitude (Amplitude):
            start_mode (str): legal values: ON, OFF
        """
        if frequency <= 0:
            raise ValueError("Oscillator.frequency cannot be <= 0")
        self.frequency = frequency
        self.last_played_sample = 0
        self.play_mode = start_mode  # legal values: ON, OFF, STOPPING

        # Build self.wave chunk, a numpy array of a full period of the wave
        self.cache_length = round(SAMPLE_RATE / self.frequency)
        factor = self.frequency * ((numpy.pi * 2) / SAMPLE_RATE)
        self.wave_cache = numpy.arange(self.cache_length)
        self.wave_cache = numpy.sin(self.wave_cache * factor) * 65535

        if amplitude:
            self.amplitude = amplitude
        else:
            change_rate_weights = [
                (0.0000001, 10000),
                (0.00001, 100),
                (0.0001, 10),
                (0.001, 0.1)]
            self.amplitude = Amplitude(
                0, change_rate_weights=change_rate_weights)

    def get_samples(self, sample_count):
        """
        Fetch a number of samples from self.wave_cache

        Args:
            sample_count (int): Number of samples to fetch

        Returns: ndarray
        """
        if self.play_mode == 'OFF' or self.amplitude.value <= 0:
            return None

        rolled_array = numpy.roll(self.wave_cache,
                                  -1 * self.last_played_sample)
        full_count, remainder = divmod(sample_count, self.cache_length)
        final_subarray = rolled_array[:remainder]
        return_array = numpy.concatenate((numpy.tile(rolled_array, full_count),
                                          final_subarray))

        self.last_played_sample = ((self.last_played_sample + remainder) %
                                   self.cache_length)
        return return_array * self.amplitude.value
