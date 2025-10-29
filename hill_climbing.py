# This file is for Person A to implement all Hill Climbing variants.

from algorithm_base import SearchAlgorithm
from data_structures import State

class SteepestAscentHillClimbing(SearchAlgorithm):
    def search(self) -> State:
        print("Running Steepest Ascent Hill Climbing... (Not Implemented)")
        # Person A: Your implementation goes here.
        # Remember to call self._start_timer() and self._stop_timer()
        # and to update self.statistics.
        self.solution = self.initial_state # Placeholder
        return self.solution

# Person A: Add other Hill Climbing classes here, e.g.:
# class HillClimbingWithSidewaysMove(SearchAlgorithm): ...
