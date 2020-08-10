from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from board.models import Article, User, Comment
# from django.core.cache import cache
from board.forms import ArticleForm, CommentForm
from django.core.serializers import serialize
import datetime
import json

def save_session(request, user_id, user_pw):
    request.session['user_id'] = user_id
    request.session['user_pw'] = user_pw

# 글 목록 보기
def list(request):
    user = request.session.get('user_id')
    if not user:
        return render(request, 'login.html')
    board_list = Article.objects.all().order_by('-id')
    context = {'article_list': board_list}
    return render(request, 'board_list.html', context)

# 게시판 상세내용 보기, 조회수 증가
def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.click_num += 1
    article.save()
    comments = article.comment_set.all()
    comments_form = CommentForm()
    context = {'article': article, 'comments_form': comments_form, 'comments': comments}
    return render(request, 'board_detail.html', context)

def create(request):
    if request.method == "POST":
        # POST 방식으로 호출될 때
        article = Article(writer=request.session.get('user_id'))
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            article_form.save()
            return HttpResponseRedirect(reverse('board:detail', args=(article.id,)))
    else:
        # GET 방식으로 호출될 때
        article_form = ArticleForm()
    return render(request, 'board_write.html', {'article_form': article_form})


def update(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == "POST":
        # POST 방식으로 호출될 때
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            article_form.save()
            #return render(request, 'board_detail.html', {'article_form': article_form, 'article': article})
            return HttpResponseRedirect(reverse('board:detail', args=(article.id,)))
    else:
        # GET 방식으로 호출될 때
        article_form = ArticleForm(instance=article)
    return render(request, 'board_edit.html', {'article_form': article_form, 'article': article})

# like 수 증가
def like(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.like_num += 1
    article.save()
    context = {
        'like_num': article.like_num,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

# unlike 수 증가
def unlike(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.unlike_num += 1
    article.save()
    context = {
        'unlike_num': article.unlike_num,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")


# article delete
def delete(request, article_id):
    Article.objects.get(pk=article_id).delete()
    return redirect('board:list')

# login
def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST["username"])
            password = user.password
        except (KeyError, User.DoesNotExist):
            message = {'message': '존재하지 않는 아이디입니다.'}
            return render(request, 'login.html', message)
        else:
            if password != request.POST["password"]:
                message = {'message': '비밀번호가 틀렸습니다.'}
                return render(request, 'login.html', message)
            else:
                save_session(request, request.POST["username"], request.POST["password"])
                return redirect('board:list')
    else:
        return render(request, 'login.html')


# logOut
def logOut(request):
    request.session.clear()
    return redirect('board:list')

# signUp
def signUp(request):
    if request.method == "POST":
        password = request.POST["password"]
        verify_password = request.POST["verify_password"]
        print(password)
        print(verify_password)
        if ( password != verify_password ):
            url = 'sign_up.html'
            message = {'message': '비밀번호를 확인해주세요.'}
            return render(request, url, message)

        try:
            user = User.objects.get(username=request.POST["username"])
        except (KeyError, User.DoesNotExist):
            user = User.objects.create(
                    username=request.POST["username"], password=request.POST["password"]
                )
            user.save()
            url = 'login.html'
            message = {'message': '회원가입이 완료되었습니다.'}
        else:
            url = 'sign_up.html'
            message = {'message': '이미 존재하는 아이디입니다.'}
        return render(request, url, message)
    else:
        return render(request, 'sign_up.html')

# comments
def addComment(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comment = Comment(article_id=article, writer=request.session.get('user_id'), write_date=datetime.datetime.now())
    comments_form = CommentForm(request.POST, instance=comment)
    if comments_form.is_valid():
        comments_form.save()
        # comments_form = CommentsForm()

    context = {
        'comment_id': comment.id,
        'comment': comment.comment,
        'writer': comment.writer,
        'write_date': comment.write_date.strftime("%Y-%m-%d %H:%M")
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

def deleteComment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    context = {
        'comment_id': comment.id,
     }
    comment.delete()
    return HttpResponse(json.dumps(context), content_type="application/json")