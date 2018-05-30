from django.contrib import admin
from .models import Article, Category, Tag, user,reply
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'user_paw')
    list_per_page = 10
    search_fields = ("user_name",)


class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content')  # 给content字段添加富文本
    list_display = ('id', 'title', 'views', 'pub_time', 'category', 'use',)
    list_editable = ("title", "views")
    list_per_page = 10
    search_fields = ("title",)


class ReplayAdmin(admin.ModelAdmin):

    list_display = ('bbs_id', 'user_id', 'content', 'time')
    list_editable = ("content",)
    list_per_page = 10
    search_fields = ("content",)


# class PostAdmin(SummernoteModelAdmin):
#     summernote_fields = ('content',)  # 给content字段添加富文本


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(user, UserAdmin)
admin.site.register(reply, ReplayAdmin)
admin.site.register(Article, ArticleAdmin)
# admin.site.register(Article, PostAdmin)