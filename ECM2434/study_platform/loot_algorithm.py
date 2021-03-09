from random import choices, choice
import json


class TierAllocator:
    def __init__(self):
        filename = r"C:\Users\Bethany\OneDrive\Documents\GitHub\ECM2434_GroupH\ECM2434\study_platform\tier_stats.json"
        with open(filename, 'r') as file:
            json_file = json.load(file)
            self.tiers = list(json_file.keys())
            self.json = json_file
            self.probs = []

            for t in self.tiers:
                self.probs.append(self.json[t]['probability'])

class LootAllocator:
    def __init__(self):
        filename = r"C:\Users\Bethany\OneDrive\Documents\GitHub\ECM2434_GroupH\ECM2434\study_platform\rewards_json.json"
        with open(filename, 'r') as file:
            json_file = json.load(file)
            self.json = json_file


def choose_tier():
    alloc = TierAllocator()

    draw = choices(alloc.tiers, alloc.probs, k=1)
    return draw[0]

def get_loot():
    t = choose_tier()
    alloc = LootAllocator()

    potential = list(alloc.json[t].keys())

    reward = choice(potential)
    reward_url = alloc.json[t][reward]

    return reward_url, reward

get_loot()