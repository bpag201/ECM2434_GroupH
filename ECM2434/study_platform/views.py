from django.shortcuts import render
from .utils import paging, get_page


def index(request):
    return render(request, 'BootstrapPractice/index.html')


def test(request):
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
    if request.GET.get("pg_num"):
        pg_num = int(request.GET.get("pg_num"))
    else:
        pg_num = 1
    pg_obj = get_page(pg_num, pars2)
    output = {
        "card_sets": pg_obj,
        "pg_size": len(pars2),
        "cur_page": pg_num
    }
    return render(request, 'BootstrapPractice/TestPage.html', output)


def test2(request):
    return render(request, 'BootstrapPractice/test2.html')
