# This file is for Person C to implement the Genetic Algorithm.

from algorithm_base import SearchAlgorithm
from data_structures import State

class GeneticAlgorithm(SearchAlgorithm):
    def search(self) -> State:
        print("Running Genetic Algorithm... (Not Implemented)")
        # Person C: Your implementation goes here.
        # Remember to call self._start_timer() and self._stop_timer()
        # and to update self.statistics.
        self.solution = self.initial_state # Placeholder
        return self.solution
