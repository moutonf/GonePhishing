from django.contrib import admin
from .models import  members, victims,groups,users

admin.site.register(members)
admin.site.register(victims)
admin.site.register(users)
admin.site.register(groups)