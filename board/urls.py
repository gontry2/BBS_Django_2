from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.list, name='list'), # 글목록
    # CRUD
    path('create/', views.create, name='create'), # 글 작성
    path('<int:article_id>/', views.detail, name='detail'),  # 글 상세내용
    path('article/<int:article_id>/delete/', views.delete, name='delete'), # 글 지우기
    path('article/<int:article_id>/update/', views.update, name='update'), # 글 수정

    path('article/<int:article_id>/like/', views.like, name='like'),  # 좋아요 숫자 증가
    path('article/<int:article_id>/unlike/', views.unlike, name='unlike'),  # 싫어요 숫자 증가

    # 회원정보
    path('login/', views.login, name='login'), # 로그인
    path('logOut/', views.logOut, name='logOut'), # 로그아웃
    path('signUp/', views.signUp, name='signUp'), # 회원가입

    # 코멘트
    path('article/<int:article_id>/addComment/', views.addComment, name='addComment'), # 코멘트 추가
    path('article/<int:comment_id>/deleteComment/', views.deleteComment, name='deleteComment'), # 코멘트 삭제
]
