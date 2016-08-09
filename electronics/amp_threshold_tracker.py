class AmpThresholdTracker:
    """
    A tracker for determining if an amplitude has crossed a threshold.
    """
    # TODO: This class is confusing and probably not necessary
    amp_threshold = 0.47
    below_threshold_cutoff_dur = 5

    def __init__(self):
        self.last_threshold_cross_time = 0

    def crosses_threshold(self, amplitude):
        return amplitude > self.amp_threshold
