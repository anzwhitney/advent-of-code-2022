import sys
from collections import defaultdict

def print_usage():
    print("Usage: python most_calories.py input_filename")
    sys.exit(0)

def parse_elves(f):
    """Parse a list of elves' calorie inventories from an iterable f."""
    elf_id = 0
    elves = defaultdict(list)
    for line in f:
        # a blank line indicates a new elf's inventory
        if line == "\n":
            elf_id += 1
        # consecutive non-blank lines are appended to the current elf's
        # inventory
        else:
            elves[elf_id].append(int(line))

    return elves

def most_calories(elves):
    """Determine the index and calorie total of the elf with the most calories.
    """
    max_cals = 0
    max_elf = None

    for elf_id, inventory in elves.items():
        cals = sum(inventory)
        if cals > max_cals:
            max_cals = cals
            max_elf = elf_id

    return max_elf, max_cals

if __name__ == "__main__":
    if sys.argv[1] == "help":
        print_usage()
    input_filename = sys.argv[1]

    try:
        f = open(input_filename, "r")
    except FileNotFoundError:
        print(f"File '{input_filename}' not found.")
        print_usage()

    elves = parse_elves(f)
    elf_id, cals = most_calories(elves)
    print(f"Elf #{elf_id} is carrying the most calories ({cals}).")
