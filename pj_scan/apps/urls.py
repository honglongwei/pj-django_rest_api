# -*- coding:utf-8 -*-
from django.conf.urls import  url
from . import views

urlpatterns = [
    url(r'^alldata/$', views.TaskList.as_view(), name='task_list'),
    url(r'^application/deviceInterface/runScanInfo', views.scan_task, name='scan_task'),
    #url(r'^application/deviceInterface/runScanInfo/$', views.get_start, name='scan_task'),
    #url(r'^application/deviceInterface/getDeviceInfo/(?P<pk>[0-9]+)$', views.get_detail, name='get_detail'),
    url(r'^application/deviceInterface/getDeviceInfo/(?P<id>[0-9]+)$', views.get_detail, name='get_detail'),
    #url(r'^application/deviceInterface/getDeviceInfo/(?P<ip>((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))))/$', views.get_detail, name='get_detail'),
]
