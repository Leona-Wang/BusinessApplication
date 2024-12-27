from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 設置默認的 Django 配置模組
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BusinessApplication.settings')

app = Celery('BusinessApplication')

# 從 Django 配置中加載 Celery 設置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 發現並自動加載 tasks.py 中的任務
app.autodiscover_tasks()
