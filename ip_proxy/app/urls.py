from django.conf.urls import url


from app import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^left/', views.left, name='left'),
    url(r'^head/', views.head, name='head'),
    url(r'^ip_list/(\d+)/$', views.ip_list, name='ip_list'),
    url(r'^search/', views.ip_search, name='ip_search'),
    url(r'^detial/', views.detial, name='detial')
]
