from data_structures import State, Item, Container

# Define large penalties for constraint violations
OVERFILL_PENALTY_MULTIPLIER = 1000000
FRAGILE_PENALTY = 500000
INCOMPATIBLE_PENALTY = 500000

# Define the threshold for fragile items
FRAGILE_THRESHOLD = 50

def calculate_objective(state: State) -> float:
    """Calculates the objective score for a given state."""
    total_score = 0.0

    # --- Mandatory Penalties ---
    overfill_penalty = 0.0
    for container in state:
        if container.current_load() > container.capacity:
            overfill_penalty += (container.current_load() - container.capacity) * OVERFILL_PENALTY_MULTIPLIER
    
    # --- Bonus Penalties ---
    fragile_penalty_score = 0.0
    incompatible_penalty_score = 0.0
    for container in state:
        # Bonus: Fragile item constraint
        fragile_items_present = [item for item in container.items if item.fragile]
        if fragile_items_present:
            other_items_load = sum(item.size for item in container.items if not item.fragile)
            if other_items_load > FRAGILE_THRESHOLD:
                fragile_penalty_score += FRAGILE_PENALTY

        # Bonus: Incompatible items constraint
        item_types = {item.item_type for item in container.items if item.item_type is not None}
        if len(item_types) > 1:
            incompatible_penalty_score += INCOMPATIBLE_PENALTY

    # --- Final Score Calculation ---
    # The primary score is the number of containers used.
    container_score = len(state)

    total_score = container_score + overfill_penalty + fragile_penalty_score + incompatible_penalty_score
    
    return total_score
