def shared_item(rucksacks):
    """Find the item type that appears in all provided rucksacks/compartments.
    In valid inputs there should be exactly one such item type.

    Args:
        rucksacks: string, sequences of item types indicated by letters.

    Returns: char, shared item between the given rucksacks or compartments.

    Raises: ValueError if there is not exactly one shared item.
    """

    shared = set(rucksacks[0]).intersection(*rucksacks)
    if len(shared) != 1:
        raise ValueError(
            f"Invalid inputs '{rucksacks}' contain {len(shared)} shared items; must contain exactly one shared item.")

    return shared.pop()


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


def calculate_shared_priority(rucksacks):
    """Sum the priorities of the shared items in all rucksacks.
    There should be exactly one shared item type in each rucksack (where
    "shared item" refers to an item type that appears in both compartments of
    the same rucksack).

    Args:
        rucksacks: string iterable, each string a rucksack representation as
        described above.

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
        # This rucksack representation is divided into two compartments at the
        # halfway point.
        size = len(rucksack)
        if size % 2 != 0:
            raise ValueError(
                f"Compartments must be the same size, found invalid rucksack of size {size}.")
        first_compartment = set(rucksack[:size//2])
        second_compartment = set(rucksack[size//2:])
        shared = shared_item([first_compartment, second_compartment])
        total += priority(shared)

    return total


def calculate_badge_priority(rucksacks, group_size=3):
    """Sum the priorities of the badges of all groups of rucksacks.
    The badge is the unique item shared between all members of the group.

    Args:
        rucksacks: string iterable, each string a rucksack representation as
        described above.
        group_size: int, default 3, the size of each group with a shared badge.

    Returns: int, sum of priorities of all badges.
    """
    # The below algorithm needs to index into rucksacks, so turn it into a list
    # (in case it's some other kind of iterable that's not indexable)
    rucksacks = list(rucksacks)
    total = 0
    for i in range(0, len(rucksacks), group_size):
        group = []
        for j in range(group_size):
            # Remove trailing newlines
            items = rucksacks[i+j].rstrip()
            # Ignore empty lines
            if not items:
                continue
            group.append(items)
        badge = shared_item(group)
        total += priority(badge)

    return total


def print_usage_and_exit(code):
    print("Usage: python3 rucksacks.py command input_filename")
    print("Available commands: shared, badge")
    print("Use 'python3 rucksacks.py help command' for details on a specific command.")
    sys.exit(code)


def shared_help():
    print("Usage: python3 rucksacks.py shared input_filename")
    print("shared calculates the sum of priorities of the items shared between compartments of each rucksack.")
    sys.exit(0)


def badge_help():
    print("Usage: python3 rucksacks.py badge input_filename")
    print("badge calculates the sum of priorities of the badge items for each group of three elves.")
    sys.exit(0)


def read_file(filename):
    try:
        f = open(filename, 'r')
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        print_usage_and_exit(1)

    return f


if __name__ == "__main__":
    import sys

    match sys.argv[1]:
        case "help":
            print_usage_and_exit(0)
        case "shared":
            if sys.argv[2] == "help":
                shared_help()
            else:
                # If not "help", sys.argv[2] should be the filename to read
                f = read_file(sys.argv[2])
                total_priority = calculate_shared_priority(f)
                print(
                    f"The total priority of all shared items is {total_priority}.")
                sys.exit(0)

        case "badge":
            if sys.argv[2] == "help":
                badge_help()
            else:
                # If not "help", sys.argv[2] should be the filename to read
                f = read_file(sys.argv[2])
                badge_priority = calculate_badge_priority(f)
                print(
                    f"The total priority of all groups' badges is {badge_priority}.")
                sys.exit(0)
