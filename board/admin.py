from django.contrib import admin
from board.models import Article, User, Comment

# Register your models here.
admin.site.register(Article)
admin.site.register(User)
admin.site.register(Comment)


