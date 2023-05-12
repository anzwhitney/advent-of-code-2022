import most_calories as mc
import pytest

# sample input from puzzle statement
fake_file = [
    "1000\n",
    "2000\n",
    "3000\n",
    "\n",
    "4000\n",
    "\n",
    "5000\n",
    "6000\n",
    "\n",
    "7000\n",
    "8000\n",
    "9000\n",
    "\n",
    "10000\n"]


def test_parse_elves():
    inventories = mc.ElfInventories()
    inventories.parse_elves(fake_file)
    assert inventories._elves == {
        0: [1000, 2000, 3000],
        1: [4000],
        2: [5000, 6000],
        3: [7000, 8000, 9000],
        4: [10000]}


def test_print_top_n(capsys):
    inventories = mc.ElfInventories()
    inventories.parse_elves(fake_file)

    # default with n = 3
    inventories.print_top_n()
    captured = capsys.readouterr()
    # multiline string literals in python are a pain, so let's join a list
    # of the individual lines with a newline as separator (still need to make
    # the final newline explicit).
    assert captured.out == "\n".join(
        ["The top 3 elves by calorie total are:",
         "0. Elf #3 (24000 cals)",
         "1. Elf #2 (11000 cals)",
         "2. Elf #4 (10000 cals)",
         "Altogether, that's 45000 calories.\n"])
