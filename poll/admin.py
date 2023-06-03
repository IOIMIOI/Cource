from django.contrib import admin

from .models import *
admin.site.register(Testing)
admin.site.register(Choice)
admin.site.register(Poll)
admin.site.register(Vote)