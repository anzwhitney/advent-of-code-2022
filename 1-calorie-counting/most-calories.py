import sys
from collections import defaultdict

def print_usage():
    print("Usage: python most_calories.py input_filename")
    sys.exit(0)

def parse_elves(f):
    elf_id = 0
    elves = defaultdict(list)
    for line in f:
        # a blank line indicates a new elf's inventory
        if line == "":
            elf_id += 1
        # consecutive non-blank lines are appended to the current elf's
        # inventory
        else:
            elves[elf_id].append(int(line))

    return elves

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
