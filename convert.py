#!/usr/bin/env python3

import re
import sys


def swap_first_last_names(name):
    """ Take 'Last, First' and return 'First Last' """
    # Take "Lastname, Firstname" and return "Firstname Lastname"
    parts = name.split(',')
    # Strip the space between comma and firstname
    parts = [p.strip() for p in parts]
    return f"{parts[1]} {parts[0]}"


def parse_name_opponent_id(row):
    """ Parse the player name and list of opponent ids """

    # Crufty regex to match things name-like things at the start of each line
    name = re.findall('^[A-Za-z,\- ]*', row)[0]
    name = name.rstrip()

    # Now remove what has been matched
    row = row.replace(name, '').lstrip()
    # Replace "Lastname, Firstname" with "Firstname Lastname"
    name = swap_first_last_names(name)
    # Split as rating and opponent ids
    values = row.split()
    # Slice everything after the rating
    values = values[1:]
    oppos = [int(x) for x in values]

    # Return player name and list of oppenent ids
    return name, oppos


def main(filename):
    """Read tsh data file line-by-line and convert to a csv file of game scores"""
    # Use dictionary for lookkup of players, opponents and scores
    players = {}
    opponents = {}
    scores = {}
    # Need to transpose and iterate over games of each player so use a list (of lists)
    starts = []

    # Read file line by line
    with open(filename, "r") as f:
        id = 0 # player id
        for row in f:
            id = id + 1 # index players from 1...

            row = row.strip()
            data = row.split(';')

            # Parse player names and opponent ids
            name, oppos = parse_name_opponent_id(data[0])
            players[id] = name
            opponents[id] = oppos

            # Parse the list of scores for each games
            ss = [int(x) for x in data[1].split()]
            scores[id] = ss

            # Parse start/reply data
            st = data[6].lstrip().split()
            st = [int(x) for x in st[1:]]
            starts.append(st)

        # Transpose starts to allow iteration through all first games, second games etc
        vstarts = list(zip(*starts))

        # Iterate over all games in each round and only process starter player
        # r, round index; rnd, round data
        for r, rnd in enumerate(vstarts, 1):
            # p, player id, g, game starter/reply flag
            for p, g in enumerate(rnd, 1):
                # Find starters
                if g == 1:
                    # Lookup opponent id, and scores for p1 and p2
                    o = opponents[p][r-1]
                    s1 = scores[p][r-1]
                    s2 = scores[o][r-1]

                    print(f"A,{r},{players[p]},{s1},{players[o]},{s2}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("provide a tsh data file, eg. a.t")
        sys.exit(1)

    main(sys.argv[1])

