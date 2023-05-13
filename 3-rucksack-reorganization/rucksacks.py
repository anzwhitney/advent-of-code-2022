def shared_items(rucksack):
    """Find the item types that appear in both compartments.
    In valid inputs there should be exactly one such item type.

    Args:
        rucksack: string, sequence of item types indicated by letters.

    Returns: set, intersection of the two compartments of the rucksack.
    """
    # This rucksack representation is divided into two compartments at the
    # halfway point.
    size = len(rucksack)
    if size % 2 != 0:
        raise ValueError(
            f"Compartments must be the same size, found invalid rucksack of size {size}.")
    first_compartment = set(rucksack[:size//2])
    second_compartment = set(rucksack[size//2:])

    return first_compartment & second_compartment


def priority(item):
    """Determine the priority of a given item type.
    Items represented by a-z have priorities 1-26; items represented by A-Z
    have priorities 27-52.

    Args:
        item: char, must be in [a-zA-Z].

    Returns: int, priority of the given item type.
    """
    asc = ord(item)

    # Translate a-z (ASCII 97-122) to priorities 1-26.
    if asc in range(97, 123):
        priority = asc - 96
    # Translate A-Z (ASCII 65-90) to priorities 27-52.
    elif asc in range(65, 91):
        priority = asc - 38
    # Valid inputs must be in one of the above ranges.
    else:
        raise ValueError(
            f"Item types must be in [a-zA-Z]; invalid item type {item}.")

    return priority


def calculate_total_priority(rucksacks):
    """Sum the priorities of the shared items in all rucksacks.
    There should be exactly one shared item type in each rucksack (where
    "shared item" refers to an item type that appears in both compartments of
    the same rucksack).

    Args:
        rucksacks: string iterable, each string a rucksack representation as
        described in shared_items().

    Returns: int, sum of priorities of all items shared between the
    compartments of each rucksack.
    """
    total = 0
    for rucksack in rucksacks:
        # Remove trailing newlines
        items = rucksack.rstrip()
        # Ignore empty lines
        if not items:
            continue
        shared = shared_items(items)
        if len(shared) != 1:
            raise ValueError(
                f"Invalid input '{rucksack}' contains {len(shared)} shared items; must contain exactly one shared item.")
        total += priority(shared.pop())

    return total


def print_usage_and_exit(code):
    print("Usage: python3 rucksacks.py input_filename")
    sys.exit(code)


if __name__ == "__main__":
    import sys

    if sys.argv[1] == "help":
        print_usage_and_exit(0)

    input_filename = sys.argv[1]
    try:
        f = open(input_filename, 'r')
    except FileNotFoundError:
        print(f"File '{input_filename}' not found.")
        print_usage_and_exit(1)

    total_priority = calculate_total_priority(f)
    print(f"The total priority of all shared items is {total_priority}.")
    sys.exit(0)
