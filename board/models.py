from django.db import models
import datetime

# Create your models here.
class Article(models.Model):
    title = models.CharField('제목',max_length=200)
    content = models.CharField('내용',max_length=1000)
    writer = models.CharField('작성자', max_length=30)
    write_date = models.DateTimeField('작성일자', default=datetime.datetime.now())
    click_num = models.IntegerField('조회수', default=0)
    like_num = models.IntegerField('좋아요', default=0)
    unlike_num = models.IntegerField('싫어요', default=0)

    def __str__(self):
        return self.title

class User(models.Model):
    username = models.CharField('아이디', max_length=30)
    password = models.CharField('패스워드', max_length=30)

    def __str__(self):
        return self.username

