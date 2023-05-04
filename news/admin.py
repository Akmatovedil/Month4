from django.contrib import admin
from news.models import News, Comment, Tag, Category


# Register your models here.


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'link', 'likes',
                    'date_off', 'category']
    search_fields = 'title'.split()
    list_filter = 'date_off category tags'.split()
    list_editable = 'category'.split()

admin.site.register(News, NewsAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Category)
