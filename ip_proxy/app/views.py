from django.core.paginator import Paginator
from django.shortcuts import render

from app.models import SsdbModel


def ip_list(request, ip_type):
    ssdb_model = SsdbModel()
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
    list_ip = [ssdb_model.to_dict(ip) for ip in list_ip]
    paginator = Paginator(list_ip, 20)
    pages = paginator.page(int(page_num))
    ctx = {
        'ip_type': ip_type,
        'pages': pages,
        'ttl': ttl_list
    }
    return render(request, 'ip_list.html', ctx)


def ip_search(request):
    ip = request.GET.get('ip')

    return render(request, 'search.html')


def index(request):

    return render(request, 'index.html')


def left(request):
    return render(request, 'left.html')


def head(request):
    return render(request, 'head.html')


def detial(request):

    return render(request, 'detial.html')


