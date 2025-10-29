import json
from data_structures import Item
from initial_state import generate_initial_state
from objective_function import calculate_objective

# Import the algorithm classes
from hill_climbing import SteepestAscentHillClimbing
from simulated_annealing import SimulatedAnnealing
from genetic_algorithm import GeneticAlgorithm

# The Algorithm Registry
ALGORITHM_REGISTRY = {
    "1": SteepestAscentHillClimbing,
    # TODO: Add other algorithms here as they are implemented
    "5": SimulatedAnnealing,
    "6": GeneticAlgorithm,
}

def print_solution(state):
    """Prints the final solution in a readable format."""
    print("\n================================")
    print(f"Total Kontainer Digunakan: {len(state)}")
    print("================================\n")
    for i, container in enumerate(state, 1):
        print(f"{i}. Kontainer {i} (Total: {container.current_load()}/{container.capacity}):")
        for item in container.items:
            details = f"- {item.id} ({item.size})"
            if item.fragile: details += " (rapuh)"
            if item.item_type: details += f" (tipe={item.item_type})"
            print(details)
        print()

def main():
    """Main function to run the interactive solver."""
    print("=== Bin Packing Problem Solver ===\n")
    print("Please choose an algorithm to run:")
    print("  1. Steepest Ascent Hill Climbing")
    print("  2. Hill Climbing with Sideways Move (Not Implemented)")
    print("  3. Stochastic Hill Climbing (Not Implemented)")
    print("  4. Random Restart Hill Climbing (Not Implemented)")
    print("  5. Simulated Annealing")
    print("  6. Genetic Algorithm")

    choice = input("\nEnter the number of the algorithm you want to use: ").strip()

    algorithm_class = ALGORITHM_REGISTRY.get(choice)
    if not algorithm_class:
        print("Invalid choice or algorithm not yet implemented.")
        return

    filepath = input("Enter the path to the JSON problem file: ").strip()

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        container_capacity = data['kapasitas_kontainer']
        items = [Item(id=d['id'], size=d['ukuran'], fragile=d.get('rapuh', False), item_type=d.get('tipe')) for d in data['barang']]
    except (FileNotFoundError, KeyError) as e:
        print(f"Error loading file: {e}")
        return

    initial_state = generate_initial_state(items, container_capacity)
    print(f"\nGenerated initial state with {len(initial_state)} containers.")
    print(f"Initial score: {calculate_objective(initial_state)}")

    # TODO: Handle algorithm-specific parameters (e.g., ask for sideways moves)

    algorithm_instance = algorithm_class(initial_state)
    
    print("--- Searching for optimal solution... ---")
    solution = algorithm_instance.search()
    stats = algorithm_instance.statistics
    print(f"--- Search Complete in {stats['duration_seconds']:.2f} seconds ---")

    print_solution(solution)

if __name__ == "__main__":
    main()
