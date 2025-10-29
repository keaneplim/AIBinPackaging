from .data_structures import Item, Container, State

def generate_initial_state(items: list[Item], container_capacity: int) -> State:
    """Generates an initial state using the First Fit heuristic."""
    state: State = [Container(container_capacity)]

    for item in items:
        placed = False
        # Tempatkan item di container yang sudah ada
        for container in state:
            if container.remaining_capacity() >= item.size:
                container.add_item(item)
                placed = True
                break
        
        # Jika tidak dapat ditempatkan, buat container baru
        if not placed:
            new_container = Container(container_capacity)
            new_container.add_item(item)
            state.append(new_container)
            
    return state
