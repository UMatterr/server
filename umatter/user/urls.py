from django.urls import path

from .views import kakao_login, kakao_callback, KakaoLogin, RegisterAPIView 




urlpatterns = [
    path(
        route='register',
        view=RegisterAPIView.as_view(),
        name='register'
    ),
    path(
        route='kakao/login',
        view=kakao_login,
        name='kakao_login',
    ),
    path(
        route='kakao/login/callback/',
        view=kakao_callback,
        name='kakao_callback',
    ),
    path(
        route='kakao/login/finish/',
        view=KakaoLogin.as_view(),
        name='kakao_login_todjango',
    ),
]
