from django.contrib import admin
from django.contrib.admin import ModelAdmin

from app import models


class NewsModelAdmin(ModelAdmin):
    list_display = ('title', 'description', 'image_url',
                    'category', 'comments', 'votes')


admin.site.register(models.NewsModel, NewsModelAdmin)