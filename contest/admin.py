from django.contrib import admin
from .models import team
from .models import question
from .models import timeRemaining

# Register your models here.
admin.site.register(team)
admin.site.register(question)
admin.site.register(timeRemaining)