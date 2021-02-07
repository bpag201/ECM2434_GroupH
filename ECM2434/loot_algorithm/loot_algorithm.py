from random import choices
import json


class TierAllocator:
    def __init__(self):
        filename = "loot_json.json"
        with open(filename, 'r') as file:
            json_file = json.load(file)
            self.tiers = json_file.keys()
            self.json = json_file
            self.probs = []

            for t in self.tiers:
                self.probs.add(self.json[t]['probability'])


def choose_tier():
    alloc = TierAllocator()
    t = check_guarantee(alloc)

    if t is not None:
        return t
    else:
        draw = choices(alloc.tiers, alloc.probs, k=1)
        return draw[0]


def check_guarantee(alloc):
    for t in alloc.tiers:
        if alloc.json[t]['wait'] == alloc.json[t]['guarantee']:
            return t
