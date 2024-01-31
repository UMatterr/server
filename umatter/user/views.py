import logging

from django.http import (
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework import status

from core.utils import get_env
from umatter.settings import BASE_URL, CLIENT_BASE_URL

from .services import (
    create_redirect_uri_to_authorize,
    create_user_with_kakao_info,
    delete_cookies,
    get_access_token_by_refresh_token,
    get_access_token_from_kakao,
    get_kakao_info_with_access_token,
    get_user_by_kakao_id,
    logout_and_remove_token,
    set_cookies_for_login,
    update_kakao_refresh_token,
)
from .utils import auth_user, control_request_method


logger = logging.getLogger("user.views")

@control_request_method()
def kakao_login(request):

    scope = get_env("AUTH_KAKAO_SCOPE")

    url = create_redirect_uri_to_authorize(scope)
    rsp = HttpResponseRedirect(url)

    return rsp


@control_request_method()
def kakao_callback(request):
    code = request.GET.get("code")

    # code로 access token 요청
    kakao_rsp = get_access_token_from_kakao(code)
    if kakao_rsp is None:
        return JsonResponse(
            {'msg': 'failed to get user infor from kakao'},
            status=status.HTTP_400_BAD_REQUEST
        )

    access_token = kakao_rsp["access_token"]
    refresh_token = kakao_rsp["refresh_token"]

    # access token으로 카카오톡 프로필 요청
    rsp = get_kakao_info_with_access_token(access_token)

    if rsp["kakao_profile"] is None:
        logger.error(
            f"return value from kakao: {rsp['kakao_rsp']}"
        )
        return JsonResponse(
            {'msg': 'failed to find kakao account profile'},
            status=status.HTTP_400_BAD_REQUEST
        )

    kakao_id = rsp["kakao_id"]
    email = rsp["email"]
    kakao_nickname = rsp["kakao_nickname"]
    profile_thumbnail = rsp["profile_thumbnail"]

    if kakao_id is None:
        return JsonResponse(
            {'msg': 'failed to find kakao id'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 이메일 없으면 오류 => 카카오톡 최신 버전에서는 이메일 없이 가입 가능해서 추후 수정해야함
    if email is None:
        return JsonResponse(
            {'msg': 'failed to get email'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = get_user_by_kakao_id(kakao_id)
    if user is None:
        return JsonResponse(
            {'msg': 'failed to get user info'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if user == 1:
        user = create_user_with_kakao_info(
            kakao_id=kakao_id,
            email=email,
            kakao_nickname=kakao_nickname,
            profile_thumbnail=profile_thumbnail,
            kakao_refresh_token=refresh_token,
        )
        logger.info(f"Created user: {type(user)} {user}")

    if user.kakao_refresh_token != refresh_token:
        user = update_kakao_refresh_token(
            user=user,
            kakao_refresh_token=refresh_token,
        )

    rsp = HttpResponseRedirect(CLIENT_BASE_URL + '/friend/info')
    rsp = set_cookies_for_login(
        rsp,
        access_token,
        refresh_token,
    )

    return rsp


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    callback_url = BASE_URL + get_env("AUTH_KAKAO_REDIRECT_URI_PATH")
    client_class = OAuth2Client


@control_request_method()
def kakao_logout(request):

    is_logged_in = request.COOKIES.get("isLoggedIn")
    refresh_token = request.COOKIES.get("refreshToken")
    if is_logged_in:
        logger.info(f"refresh token for logout: {refresh_token}")
        logout_and_remove_token(refresh_token=refresh_token)
        rsp = HttpResponseRedirect(CLIENT_BASE_URL)
        rsp = delete_cookies(rsp)

        return rsp

    return redirect(CLIENT_BASE_URL)


@auth_user
@control_request_method()
def refresh_kakao_access_token(request):
    refresh_token = request.COOKIES.get("refreshToken")
    access_token = get_access_token_by_refresh_token(refresh_token)
    rsp = HttpResponseRedirect(CLIENT_BASE_URL)
    rsp = set_cookies_for_login(
        rsp=rsp,
        access_token=access_token,
    )
    return rsp
