from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('db', views.db, name='updateDB'),
    path('get_city_code', views.get_city_code),
    path('get_seoul_route', views.get_seoul_route),
    path('get_busan_route', views.get_busan_route),
    path('get_nation_route', views.get_nation_route),
    path('get_seoul_bus', views.get_seoul_bus),
    path('get_busan_bus', views.get_busan_bus),
    path('get_nation_bus', views.get_nation_bus),
    path('get_seoul_company', views.get_seoul_company),
    path('get_busan_company', views.get_busan_company),
    path('get_nation_company', views.get_nation_company),
    path('seoul_route', views.seoul_route, name='seoul_route'),
    path('busan_route', views.busan_route, name='busan_route'),
    path('nation_route', views.nation_route, name='nation_route'),
    path('nation_route/<int:city_code>/', views.nation_route_detail, name='nation_route_detail'),
    path('seoul_company', views.seoul_company, name='seoul_company'),
    path('busan_company', views.busan_company, name='busan_company'),
    path('nation_company', views.nation_company, name='nation_company'),
    ]


