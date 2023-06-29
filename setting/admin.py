from django.contrib import admin

# Register your models here.

from common.models import User
from todo.models import Todo, DoneDays
admin.site.register(User)
admin.site.register(Todo)
admin.site.register(DoneDays)
