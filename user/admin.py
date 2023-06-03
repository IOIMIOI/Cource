from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
admin.site.site_title = 'Админ-панель платформы'
admin.site.site_header = 'Админ-панель платформы 2'

admin.site.register(Profile)

