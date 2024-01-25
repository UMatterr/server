from django.urls import path

from .views import (
    kakao_callback,
    kakao_login,
    kakao_logout,
    refresh_kakao_access_token,
    KakaoLogin,
)


urlpatterns = [
    path(
        route='login',
        view=kakao_login,
        name='kakao_login',
    ),
    path(
        route='logout',
        view=kakao_logout,
        name='kakao_logout',
    ),
    path(
        route='refresh',
        view=refresh_kakao_access_token,
        name='kakao_refresh',
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
