
from collections import Counter, OrderedDict
from itertools import chain
import csv
import sys


def display_inventory(inventory):
    """Displays the items and their number of occurences
    in the inventory and sums up all."""
    print("Inventory:")
    for key, value in inventory.items():
        print(value, key)
    print("Total number of items: {}".format(sum(inventory.values())))


def add_to_inventory(inventory, added_items):
    """Adds a given list of loot to the inventory.
    A temporary list is used to avoid adding the count
    of each items occurence more than once."""
    temp_list = []
    for item in added_items:
        if item not in temp_list:
            temp_list.append(item)
            if item in inventory:
                inventory[item] += added_items.count(item)
            else:
                inventory[item] = added_items.count(item)
    return inventory


def longest(inventory):
    """Returns the longest string of the inventory"""
    longest_str = 0
    for item in inventory:
        if len(str(item)) > longest_str:
            longest_str = len(str(item))
    return longest_str


def print_line(sign):
    """Prints customizable lines. (Only one character is allowed!)"""
    print((l_width+r_width+1)*sign)


def print_items(inventory):
    """Right-justifies the two (value + key) columns."""
    for key, value in inventory.items():
        print(str(value).rjust(l_width),
              key.rjust(r_width))


def print_table(inventory, order=None):
    """Prints the table according to given order (or non-order).
    Possible order parameters: "count,asc", "count,desc", None.
    Gives an error message if the parameter is not correct."""
    global l_width
    global r_width
    l_width = longest(inventory.values()) + 3
    r_width = longest(inventory.keys()) + 3
    print("Inventory:")
    print("count".rjust(l_width),
          "item name".rjust(r_width))
    print_line("⯎")
    if order is None:  # There's no special order here.
        print_items(inventory)
    elif order == "count,asc":  # Ordering items in ascending order.
        inv_asc = OrderedDict(sorted(inventory.items(),
                              key=lambda x: x[1]))
        print_items(inv_asc)
    elif order == "count,desc":  # Ordering items in descending order.
        inv_desc = OrderedDict(sorted(inventory.items(),
                               key=lambda x: -x[1]))
        print_items(inv_desc)
    else:  # Error message is printed if the parameter is anything else.
        print("error ☹".center(l_width+r_width))
    print_line("⯎")
    print("Total number of items: {}".format(sum(inventory.values())))


def import_inventory(inventory, filename="import_inventory.csv"):
    """Imports new items from a given .csv file.
    In case of one argument (the program itself), the function stops."""
    if len(sys.argv) > 1:  # If there is more than one argument:
        filename = sys.argv[1]  # the second one (index 1) is the file.
    else:
        return
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        reader = list(chain.from_iterable(reader))
        inventory = add_to_inventory(inventory, reader)
    return inventory


def export_inventory(inventory, filename="export_inventory.csv"):
    """Exports the items of the inventory to a .csv file.
    If filename is not given, it automatically becomes
    "export_inventory.csv"."""
    if len(sys.argv) > 2:  # If there are more than two arguments:
        filename = sys.argv[2]  # the third one (index 2) is the file.
    else:  # If there are less arguments, it creates (or overwrites) one.
        filename = "export_inventory.csv"
    with open(filename, "w") as csvfile:
        exp_inv = Counter(inventory)
        writer = csv.writer(csvfile, exp_inv.elements())
        writer.writerow(exp_inv.elements())


def main(argv):
    inv = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}
    dragon_loot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
    inv = add_to_inventory(inv, dragon_loot)

    import_inventory(inv, filename="import_inventory.csv")
    export_inventory(inv, filename="export_inventory.csv")
    print_table(inv, order=None)


if __name__ == "__main__":
    main(sys.argv)
