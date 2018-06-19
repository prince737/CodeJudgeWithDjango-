from django.contrib import admin
from .models import team
from .models import question

# Register your models here.
admin.site.register(team)
admin.site.register(question)