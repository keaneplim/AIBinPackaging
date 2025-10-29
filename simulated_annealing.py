# This file is for Person B to implement Simulated Annealing.

from algorithm_base import SearchAlgorithm
from data_structures import State

class SimulatedAnnealing(SearchAlgorithm):
    def search(self) -> State:
        print("Running Simulated Annealing... (Not Implemented)")
        # Person B: Your implementation goes here.
        # Remember to call self._start_timer() and self._stop_timer()
        # and to update self.statistics.
        self.solution = self.initial_state # Placeholder
        return self.solution
