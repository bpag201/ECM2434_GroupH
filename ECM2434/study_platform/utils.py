from django.core.paginator import Paginator

""" objects = all blogs / comments; pg_num = target page number """


def paging(objects):
    p = Paginator(objects, 3)  # how many objects in one page?
    switcher = {}
    for i in range(1, p.num_pages+1):
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
