from django.contrib import admin
from forever.models import *
# Register your models here.

admin.site.register(Todo)
admin.site.register(QRcode)
admin.site.register(UserProfile)