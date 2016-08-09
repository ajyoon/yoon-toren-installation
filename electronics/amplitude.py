from blur import rand
import numpy


def find_amplitude(chunk):
    """
    Calculate the 0-1 amplitude of an ndarray chunk of audio samples.

    Samples in the ndarray chunk are signed int16 values oscillating
    anywhere between -32768 and 32767. Find the amplitude between 0 and 1
    by summing the absolute values of the minimum and maximum, and dividing
    by 32767.

    Args:
        chunk (str): A binary string of int16 values representing audio samples

    Returns:
        float: The amplitude of the sample between 0 and 1.
            Note that this is not a decibel representation of
            the amplitude.
    """
    chunk = numpy.fromstring(chunk, numpy.int16)
    return (abs(int(chunk.max())) + abs(int(chunk.min()))) / 32767


def normalize_amplitude(chunk, amplitude):
    """
    Normalize a chunk of audio samples to a given amplitude

    Args:
        chunk (str): A binary string of int16 values representing audio samples
        amplitude (float): The amplitude to normalize to.
            Should be between 0 and 1.

    Returns:

    """
    chunk_amplitude = find_amplitude(chunk)
    modified_chunk = chunk * (amplitude / chunk_amplitude)
    return modified_chunk


class Amplitude:
    """
    A handler for audio amplitude values.
    """
    def __init__(self, init_value=0, drift_target_weights=None,
                 change_rate_weights=None, move_freq_weights=None):
        """
        Args:
            init_value (float):
            drift_target_weights (list): a list of 2-tuple weights
            change_rate_weights (list): a list of 2-tuple weights
            move_freq_weights (list): a list of 2-tuple weights
        """
        # TODO: improve docs
        # Set up amplitude
        self._raw_value = None
        self.value = init_value
        if drift_target_weights is None:
            self.drift_target_weights = [
                (-1, 1), (0.02, 6), (0.2, 1), (0.3, 0)]
        else:
            self.drift_target_weights = drift_target_weights
        self.drift_target = rand.weighted_rand(self.drift_target_weights)

        if change_rate_weights is None:
            self.change_rate_weights = [(0.00001, 100), (0.001, 5), (0.01, 1)]
        else:
            self.change_rate_weights = change_rate_weights
        self.change_rate = rand.weighted_rand(self.change_rate_weights)

        if move_freq_weights is None:
            self.move_freq_weights = [(0.000001, 10), (0.01, 1)]
        else:
            self.move_freq_weights = move_freq_weights
        self.move_freq = rand.weighted_rand(self.move_freq_weights)

    @property
    def value(self):
        """
        float: Adjusted amplitude. Sub-zero values return 0
        """
        # TODO: Is it an antipattern to set value to negative values?
        #     maybe implementation needs to be changed
        if self._raw_value < 0:
            return 0
        else:
            return self._raw_value

    @value.setter
    def value(self, new_value):
        self._raw_value = new_value

    def re_roll_behaviors(self):
        """
        Re-randomly-generate behavior attributes.

        Returns: None
        """
        self.move_freq = rand.weighted_rand(self.move_freq_weights)
        self.drift_target = rand.weighted_rand(self.drift_target_weights)
        self.change_rate = rand.weighted_rand(self.change_rate_weights)

    def step_amp(self):
        """
        Change the amplitude according to the change rate and drift target.

        Also offer a chance to re-roll behavior attributes.

        Returns: None
        """
        # Roll for a chance to change the drift target and change rate
        if rand.prob_bool(self.move_freq):
            self.re_roll_behaviors()
        # step the amplitude
        difference = self.drift_target - self.value
        if abs(difference) < self.change_rate:
            self.value = self.drift_target
        else:
            delta = self.change_rate * numpy.sign(difference)
            self.value += delta
