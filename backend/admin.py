from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from dbmodels import models


class Tran(ModelAdmin):
    list_display = ('__str__','team','img','stat','user')
    list_editable = ('team','img','stat','user',)
    ordering = ['-team',]
from django.db.models.options import Options


admin.site.register(models.ShowImg)
admin.site.register(models.Transaction,Tran)
admin.site.register(models.RightNav)
admin.site.register(models.Menu)

