from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from board.models import Article, User
from django.core.cache import cache
import datetime

# Create your views here.

# 글 목록 보기
def list(request):

    user = cache.get('user')
    if not user:
        return render(request, 'login.html')
    board_list = Article.objects.all().order_by('-id').reverse()
    context = {'article_list' : board_list, 'user': user}
    return render(request, 'board_list.html', context)

# 게시판 상세내용 보기, 조회수 증가
def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.click_num += 1
    article.save()
    user = cache.get('user')
    context = {'article' : article, 'user' : user}
    return render(request, 'board_detail.html', context)

# 글쓰기 화면으로 이동
def write(request):
    user = cache.get('user')
    return render(request, 'board_write.html', {'user': user})

# 글 내용 저장/수정
def save(request):
    try:
        article = Article.objects.get(pk=request.POST.get("article", False))
    except (KeyError, Article.DoesNotExist):
        article = Article.objects.create(
                    title=request.POST["title"], content=request.POST["content"], writer=cache.get('user').username
                )
    else:
        article.title = request.POST["title"]
        article.content = request.POST["content"]
        article.write_date = datetime.datetime.now()

    article.save()
    return HttpResponseRedirect(reverse('board:detail', args=(article.id,)))

# like 수 증가
def like(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.like_num += 1
    article.click_num -= 1
    article.save()
    return HttpResponseRedirect(reverse('board:detail', args=(article.id,)))

# unlike 수 증가
def unlike(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.unlike_num += 1
    article.click_num -= 1
    article.save()
    return HttpResponseRedirect(reverse('board:detail', args=(article.id,)))

# article delete
def delete(request, article_id):
    Article.objects.get(pk=article_id).delete()
    return HttpResponseRedirect(reverse('board:list',))

# article edit 화면으로 이동
def edit(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    user = cache.get('user')
    return render(request, 'board_edit.html', { 'article' : article, 'user' : user})

# index
def index(request):
    return render(request, 'login.html')

# login
def login(request):
    try:
        user = User.objects.get(username=request.POST["username"])
        password = user.password
    except (KeyError, User.DoesNotExist):
        return render(request, 'login.html', {'error_message' : "아이디 혹은 비밀번호가 틀렸습니다."})
        #return HttpResponseRedirect(reverse('board:index', args={'error_message' : "아이디 혹은 비밀번호가 틀렸습니다."}))
    else:
        if password != request.POST["password"]:
            return render(request, 'login.html', {'error_message' : "아이디 혹은 비밀번호가 틀렸습니다."})
            #return HttpResponseRedirect(reverse('board:index'))
        else:
            cache.set('user', user, 10000)
            return HttpResponseRedirect(reverse('board:list'))

# logOut
def logOut(request):
    cache.clear()
    return HttpResponseRedirect(reverse('board:list',))

# signUp화면으로 이동
def goToSignUp(request):
    return render(request, 'sign_up.html')

# signUp
def signUp(request):
    try:
        user = User.objects.get(username=request.POST["username"])
    except (KeyError, User.DoesNotExist):
        user = User.objects.create(
                username=request.POST["username"], password=request.POST["password"]
            )
        user.save()
        return render(request, 'login.html', {'message' : "회원가입이 완료되었습니다."})
    else:
        return render(request, 'sign_up.html', {'error_message' : "이미 존재하는 아이디입니다."})




