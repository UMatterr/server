from django.urls import path

from .views import RegisterAPIView


urlpatterns = [
    path(
        route='register',
        view=RegisterAPIView.as_view(),
        name='register'
    ),
    # path(
    #     route='kakao/login',
    #     view=kakao_login,
    #     name='google_login'
    # ),
    # path(
    #     route='kakao/callback/',
    #     view=kakao_callback,
    #     name='google_callback'
    # ),
    # path(
    #     route='kakao/login/finish/',
    #     view=KakaoLogin.as_view(),
    #     name='google_login_todjango'
    # ),
]