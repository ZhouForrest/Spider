from django.core.paginator import Paginator
from django.shortcuts import render

from app.models import SsdbModel

ssdb_model = SsdbModel()

def ip_list(request, ip_type):
    if ip_type == '0':
        list_ip = ssdb_model.get_fast_proxy()
    if ip_type == '1':
        list_ip = ssdb_model.get_yun_proxy()
    if ip_type == '2':
        list_ip = ssdb_model.get_owner_proxy()
    if ip_type == '3':
        list_ip = ssdb_model.get_other_proxy()
    page_num = request.GET.get('page_num', 1)
    ttl_list = list(map(ssdb_model.get_ttl, list_ip[(int(page_num) - 1) * 20: int(page_num) * 20]))
    ip_info = [ssdb_model.to_dict(ip) for ip in list_ip]
    for i in range(20):
        ip_info[(int(page_num) - 1) * 20 + i]['ttl'] = ttl_list[i]
    paginator = Paginator(ip_info, 20)
    pages = paginator.page(int(page_num))
    ctx = {
        'ip_type': ip_type,
        'pages': pages,
    }
    return render(request, 'ip_list.html', ctx)


def ip_search(request):
    ip = request.GET.get('ip')
    ip_types = ['0_1_', '0_2_', '0_3_', '1_', '2_', '3_', 'b_']
    list_ip = []
    for ip_type in ip_types:
        ip_info = ip_type + ip
        if ssdb_model.get_ip(ip_info):
            list_ip.extend(ssdb_model.get_ip(ip_info))
    page_num = request.GET.get('page_num', 1)
    ttl_list = list(map(ssdb_model.get_ttl, list_ip[(int(page_num) - 1) * 20: int(page_num) * 20]))
    ip_info = [ssdb_model.to_dict(ip) for ip in list_ip]
    for i in range(20):
        ip_info[(int(page_num) - 1) * 20 + i]['ttl'] = ttl_list[i]
    paginator = Paginator(ip_info, 20)
    pages = paginator.page(int(page_num))
    ctx = {
        'pages': pages,
    }
    return render(request, 'search.html', ctx)


def index(request):

    return render(request, 'index.html')


def left(request):
    return render(request, 'left.html')


def head(request):
    return render(request, 'head.html')


def detial(request):

    return render(request, 'detial.html')


