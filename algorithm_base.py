import time
from data_structures import State

class SearchAlgorithm:
    """
    A base class for all search algorithms. It defines the common interface
    and handles basic statistics.
    """
    def __init__(self, initial_state: State):
        self.initial_state = initial_state
        self.solution = None
        self.statistics = {
            "duration_seconds": 0,
            "iterations": 0,
            "score_history": []
        }

    def search(self) -> State:
        """
        This method must be implemented by each specific algorithm.
        It should run the search, update statistics, and return the best state found.
        """
        raise NotImplementedError("The search() method must be implemented by a subclass.")

    def _start_timer(self):
        self._start_time = time.time()

    def _stop_timer(self):
        self.statistics["duration_seconds"] = time.time() - self._start_time
