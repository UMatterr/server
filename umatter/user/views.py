import logging
import traceback as tb

from core.utils import get_env
from django.http import (
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework import status

import requests
from umatter.settings import BASE_URL
from .utils import auth_user
from .services import (
    create_redirect_uri_for_kakao,
    create_user_with_kakao_info,
    delete_cookies_for_logout,
    get_user_by_kakao_id,
    get_access_token_by_refresh_token,
    logout_and_remove_token,
    set_cookies_for_login,
    update_kakao_refresh_token,
)


logger = logging.getLogger("user.views")

def kakao_login(request):

    scope = get_env("AUTH_KAKAO_SCOPE")

    base_url = "https://kauth.kakao.com/oauth/authorize"
    params = {
        "response_type": "code",
        "scope": scope,
    }
    url = create_redirect_uri_for_kakao(base_url, params)
    return redirect(url)


def kakao_callback(request):
    code = request.GET.get("code")

    # code로 access token 요청
    base_url = "https://kauth.kakao.com/oauth/token"
    params = {
        "grant_type": "authorization_code",
        "code": code,
    }
    url = create_redirect_uri_for_kakao(base_url, params)

    token_request = requests.get(url)
    token_response_json = token_request.json()
    logger.info(f"token_response_json: {token_response_json}")

    # 에러 발생 시 중단
    err = token_response_json.get("error", None)
    if err is not None:
        logger.error(tb.format_exc())
        return JsonResponse(
            {'msg': 'failed to get user infor from kakao'},
            status=status.HTTP_400_BAD_REQUEST
        )

    access_token = token_response_json.get("access_token")
    refresh_token = token_response_json.get("refresh_token")
    # logger.info(f"kakao access token: {access_token}")

    # access token으로 카카오톡 프로필 요청
    res = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    kakao_res = res.json()
    logger.info(f"profile: {kakao_res}")

    kakao_id = kakao_res.get("id", None)
    kakao_account = kakao_res.get("kakao_account", None)
    email = kakao_account.get("email", None) # 이메일!
    kakao_profile = kakao_account.get("profile", None) # kakao profile!
    if kakao_profile is None:
        logger.error(f"return value from kakao: {kakao_res}")
        return JsonResponse(
            {'msg': 'failed to find kakao account profile'},
            status=status.HTTP_400_BAD_REQUEST
        )

    kakao_nickname = kakao_profile.get("nickname", None) # 닉네임!
    profile_thumbnail = kakao_profile.get("thumbnail_image_url", None) # kakao thumbnail image!

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

    rsp = HttpResponseRedirect('/')
    rsp = set_cookies_for_login(
        rsp,
        access_token,
        refresh_token,
    )
    logger.info(f"rsp: {rsp.__dict__}")

    return rsp


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    callback_url = BASE_URL + get_env("AUTH_KAKAO_REDIRECT_URI_PATH")
    client_class = OAuth2Client


def kakao_logout(request):
    refresh_token = request.COOKIES.get("refreshToken")
    logger.info(f"refresh token for logout: {refresh_token}")
    logout_and_remove_token(refresh_token=refresh_token)
    rsp = HttpResponseRedirect('/')
    rsp = delete_cookies_for_logout(rsp)

    return rsp


@auth_user
def refresh_kakao_access_token(request):
    refresh_token = request.COOKIES.get("refreshToken")
    access_token = get_access_token_by_refresh_token(refresh_token)
    rsp = HttpResponseRedirect('/')
    rsp = set_cookies_for_login(
        rsp=rsp,
        access_token=access_token,
    )
    return rsp
