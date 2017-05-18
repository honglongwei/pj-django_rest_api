# -*- coding:utf-8 -*-
from rest_framework import serializers
from .models import BaseMsg, SrvMsg, ApiMsg


class BaseMsgSerializer(serializers.ModelSerializer):
    data_set = serializers.StringRelatedField(many=True)
    class Meta:
        model = BaseMsg
        fields = ('id', 'ip', 'devlang', 'langver', 'webtype', 'webversion', 'osinfo', 'osversion', 'dbtype', 'dbversion', 's_count', 'data_set')


class SrvMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = SrvMsg
        fields = ('id', 'midport', 'midtype', 'midversion')


class ApiMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiMsg
        fields = ('id', 'ip', 'port', 'msg')
