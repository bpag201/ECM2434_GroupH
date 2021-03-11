import json
from numpy.random import choice
from django.core.paginator import Paginator

""" objects = all blogs / comments; pg_num = target page number """


def paging(objects):
    p = Paginator(objects, 3)  # how many objects in one page?
    switcher = {}
    for i in range(1, p.num_pages + 1):
        switcher[i] = p.page(i)
    return switcher


def get_page(pg_num, switcher):
    return switcher[pg_num].object_list


sample1 = {
    "Title": "Sample1",
    "Description": "zhubao zhui diao",
    "Author": "HuangJie",
    "Tags": ["HuangJie1", "HuangJie2", "HuangJie3"]
}
sample2 = {
    "Title": "Sample1",
    "Description": "zhubao zhui diao",
    "Author": "ZhuBao",
    "Tags": ["ZhuBao1", "ZhuBao2", "ZhuBao3"]
}

pars = {
    "card_sets": [sample1, sample2, sample1, sample2, sample1, sample2, sample1, sample2]
}
pars2 = paging(pars["card_sets"])


def get_user_rank(score):
    if score < 50:
        return "Grape Soldier"
    elif score < 120:
        return "Cherry Knight"
    elif score < 210:
        return "Lemon Baron"
    elif score < 320:
        return "Kiwi Viscount"
    elif score < 450:
        return "Coconut Earl "
    elif score < 600:
        return "Pineapple Marquis"
    elif score < 770:
        return "Melon Duke"


def allocate_loot():
    with open('melons/rewards.json') as f:
        items = json.load(f)
    with open('melons/tier_stats.json') as f2:
        prob_raw = json.load(f2)
    tiers = []
    prob = []
    item_list = []
    for n, p in prob_raw.items():
        tiers.append(n)
        prob.append(p['probability'])
    tier_output = choice(tiers, 6, prob)
    for t in tier_output:
        chosen_key = choice(list(items[t].keys()))
        chosen_item = items[t][chosen_key]
        item_description = chosen_item['description']
        item_url = chosen_item['url']
        item_list.append([chosen_key, item_description, item_url])
    f.close()
    f2.close()
    return item_list


def get_loot_detail(name):
    with open('melons/rewards.json') as f:
        items = json.load(f)
        for k, i in items.items():
            for j in i.keys():
                if j == name:
                    target_item = items[k][name]
                    item_description = target_item['description']
                    item_url = target_item['url']
                    return [item_description, item_url]
    f.close()
    return ['', '']
