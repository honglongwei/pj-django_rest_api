# django api使用技巧

vi settings.py
```settings
启用celery队列
import os
import djcelery
from celery import Celery, platforms
djcelery.setup_loader()
BROKER_URL= 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
platforms.C_FORCE_ROOT = True  (允许root启动：python manage.py celery worker --loglevel=info )

关闭debug
DEBUG = False
ALLOWED_HOSTS = ['192.168.1.1', '127.0.0.1'] or ALLOWED_HOSTS = ['*']

添加rest_framework和celery
INSTALLED_APPS = [
    'rest_framework',
    'apps',
    'djcelery',
    'kombu.transport.django',
]

关闭rest-api界面测试模式，只返回json
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

安全模式
python manage.py runserver 127.0.0.1:8080 --insecure

```

外键序列化
vim models.py
```models
ID =  models.ForeignKey(BaseMsg, related_name="data_set")
```
vim serializers.py
```serializers
class MsgSerializer(serializers.ModelSerializer):
    data_set = serializers.StringRelatedField(many=True)
    class Meta:
        model = Msg
        fields = ('id', 'ip', 'data_set')
```
