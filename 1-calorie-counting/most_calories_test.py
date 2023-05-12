import most_calories as mc
import pytest


def test_parse_elves():
    inventories = mc.ElfInventories()
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
    inventories.parse_elves(fake_file)
    assert inventories._elves == {
        0: [1000, 2000, 3000],
        1: [4000],
        2: [5000, 6000],
        3: [7000, 8000, 9000],
        4: [10000]}
