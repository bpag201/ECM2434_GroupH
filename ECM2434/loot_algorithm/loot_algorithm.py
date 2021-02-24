from random import choices
import json

'''
    A class that on instantiation reads the json file and stores the required data in attributes for easier access.
'''
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

'''
    Chooses the tier that the loot the user recieves belongs to. Uses the random module to produce these answers.
    Currently it only produces one value at a time, but it does provide functionality to produce more than one at once.
'''
def choose_tier():
    alloc = TierAllocator()
    t = check_guarantee(alloc)

    if t is not None:
        return t
    else:
        draw = choices(alloc.tiers, alloc.probs, k=1)
        return draw[0]

'''
    Checks whether the user has recieved a certain tier within the guaranteed number of draws. If not then
    they will be given this tier.
'''
def check_guarantee(alloc):
    for t in alloc.tiers:
        if alloc.json[t]['wait'] == alloc.json[t]['guarantee']:
            return t
