from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.list, name='list'), # 글목록
    path('<int:article_id>/', views.detail, name='detail'), # 글 상세내용
    path('write/', views.write, name='write'), # 글작성 화면으로 이동
    path('write/save/', views.save, name='save'), # 글 작성/수정 저장
    path('article/<int:article_id>/like/', views.like, name='like'), # 좋아요 숫자 증가
    path('article/<int:article_id>/unlike/', views.unlike, name='unlike'), # 싫어요 숫자 증가
    path('article/<int:article_id>/delete/', views.delete, name='delete'), # 글 지우기
    path('article/<int:article_id>/edit/', views.edit, name='edit'), # 글 수정하는 화면으로 이동
    path('index/', views.index, name='index'), # 로그인 화면으로 이동
    path('login/', views.login, name='login'), # 로그인
    path('logOut/', views.logOut, name='logOut'), # 로그아웃
    path('goToSignUp/', views.goToSignUp, name='goToSignUp'), # 회원가입화면 이동
    path('signUp/', views.signUp, name='signUp'), # 회원가입
]
