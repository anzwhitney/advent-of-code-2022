import heapq
import sys

from collections import defaultdict

class ElfInventories:

    def __init__(self):
        self._elves = defaultdict(list)
        self._cal_totals = []

    def parse_elves(self, f):
        """Parse a list of elves' calorie inventories from an iterable f."""
        elf_id = 0
        for line in f:
            # a blank line indicates a new elf's inventory
            if line == "\n":
                elf_id += 1
            # consecutive non-blank lines are appended to the current elf's
            # inventory
            else:
                self._elves[elf_id].append(int(line))

    def print_top_n(self, n=3):
        if not self._cal_totals:
            for elf_id, inventory in self._elves.items():
                heapq.heappush(self._cal_totals, (sum(inventory), elf_id))

        # TODO: determine whether this usage of nlargest actually gets the
        # benefits of the pre-heapification.
        top_n = heapq.nlargest(n, self._cal_totals)
        total = sum(cals for cals, _ in top_n)
        print(f"The top {n} elves by calorie total are:")
        for rank, elf in enumerate(top_n):
            print(f"{rank}. Elf #{elf[1]} ({elf[0]} cals)")
        print(f"Altogether, that's {total} calories.")

def print_usage():
    print("Usage: python most_calories.py input_filename")
    sys.exit(0)

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
