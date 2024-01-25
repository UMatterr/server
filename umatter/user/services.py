import logging
import traceback as tb
from urllib.parse import urlencode

import requests

from django.http import HttpResponse

from core.utils import get_env
from umatter.settings import BASE_URL
from .models import User, LoginLog


logger = logging.getLogger("user.services")


def create_redirect_uri_to_authorize(scope):
    base_url = "https://kauth.kakao.com/oauth/authorize"
    params = {
        "client_id": get_env("AUTH_KAKAO_CLIENT_ID"),
        "client_secret": get_env("AUTH_KAKAO_CLIENT_SECRET"),
        "redirect_uri": BASE_URL + get_env("AUTH_KAKAO_REDIRECT_URI_PATH"),
        "response_type": "code",
        "scope": scope,
    }
    params = urlencode(params)
    # logger.info(f"url: {base_url}?{params}")
    return f"{base_url}?{params}"


def create_user_with_kakao_info(
    kakao_id,
    email,
    kakao_nickname,
    kakao_refresh_token,
    profile_thumbnail=None,
):
    user = User.objects.create(
        kakao_id=kakao_id,
        email=email,
        kakao_nickname=kakao_nickname,
        kakao_refresh_token=kakao_refresh_token,
        profile_thumbnail=profile_thumbnail,
    )
    login_log = LoginLog.objects.create(
        user=user, login_type='i'
    )
    logger.info(f"Created user: {user}")
    logger.info(f"Created login_log: {login_log}")
    return user


def delete_cookies(rsp):
    rsp.delete_cookie('isLoggedIn')
    rsp.delete_cookie('accessToken')
    rsp.delete_cookie('refreshToken')
    return rsp


def get_access_token_by_refresh_token(refresh_token):
    base_url = "https://kauth.kakao.com/oauth/token"
    params = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": get_env("AUTH_KAKAO_CLIENT_ID"),
        "client_secret": get_env("AUTH_KAKAO_CLIENT_SECRET"),
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    rsp = requests.post(
        base_url,
        data=params,
        headers=headers
    )
    rsp = rsp.json()
    logger.info(f"return value from kakao: {rsp}")
    access_token = rsp.get("access_token")
    return access_token


def get_access_token_from_kakao(code):

    base_url = "https://kauth.kakao.com/oauth/token"
    params = {
        "client_id": get_env("AUTH_KAKAO_CLIENT_ID"),
        "client_secret": get_env("AUTH_KAKAO_CLIENT_SECRET"),
        "redirect_uri": BASE_URL + get_env("AUTH_KAKAO_REDIRECT_URI_PATH"),
        "grant_type": "authorization_code",
        "code": code,
    }
    params = urlencode(params)
    url = f"{base_url}?{params}"

    token_request = requests.get(url)
    token_response_json = token_request.json()
    logger.info(f"token_response_json: {token_response_json}")

    # 에러 발생 시 중단
    err = token_response_json.get("error", None)
    if err is not None:
        logger.error(tb.format_exc())
        return None

    access_token = token_response_json.get("access_token")
    refresh_token = token_response_json.get("refresh_token")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def get_kakao_info_with_access_token(access_token):
    rsp = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    kakao_rsp = rsp.json()
    logger.info(f"profile: {kakao_rsp}")

    kakao_id = kakao_rsp.get("id", None)
    kakao_account = kakao_rsp.get("kakao_account", None)
    email = kakao_account.get("email", None) # 이메일!
    kakao_profile = kakao_account.get("profile", None) # kakao profile!
    kakao_nickname = kakao_profile.get("nickname", None) # 닉네임!
    profile_thumbnail = kakao_profile.get("thumbnail_image_url", None) # kakao thumbnail image!

    return {
        "kakao_id": kakao_id,
        "email": email,
        "kakao_nickname": kakao_nickname,
        "profile_thumbnail": profile_thumbnail,
        "kakao_account": kakao_account,
        "kakao_profile": kakao_profile,
        "kakao_rsp": kakao_rsp,
    }


def get_user_by_kakao_id(kakao_id):
    try:
        user = User.objects.get(kakao_id=kakao_id)
        login_log = LoginLog.objects.create(
            user=user, login_type='i'
        )
        logger.info(f"Created login_log: {login_log}")
        return user

    except User.DoesNotExist:
        logger.info("Need to create an new user")
        return 1

    except User.MultipleObjectsReturned:
        logger.error("Multiple users with same kakao id")
        return None

    except:
        logger.error("Some error while getting user by kakao id")
        logger.error(tb.format_exc())
        return None


def logout_and_remove_token(refresh_token):
    try:
        user = User.objects.get(kakao_refresh_token=refresh_token)
        new_log = LoginLog.objects.create(
            user=user, login_type='o'
        )
        user.kakao_refresh_token = ""
        user.save()
        logger.info(f"Created logout log: {new_log}")
        return user

    except User.DoesNotExist:
        logger.error("No user info")
        logger.error(tb.format_exc())
        return None

    except User.MultipleObjectsReturned:
        logger.error("Multiple users with same kakao id")
        logger.error(tb.format_exc())
        return None

    except:
        logger.error("Some error while processing logout")
        logger.error(tb.format_exc())
        return None


def set_cookies_for_login(
    rsp,
    access_token=None,
    refresh_token=None,
):
    if access_token:
        rsp.set_cookie(
            key="accessToken",
            value=access_token,
            httponly=True,
        )
    if refresh_token:
        rsp.set_cookie(
            key="refreshToken",
            value=refresh_token,
            httponly=True,
        )
    rsp.set_cookie(
        key="isLoggedIn",
        value=True,
        httponly=False,
    )
    return rsp


def update_kakao_refresh_token(
    user: User,
    kakao_refresh_token: str = None,
):
    user.kakao_refresh_token = kakao_refresh_token
    user.save()
    logger.info(f"Updated refresh token: {user}")
    return user


def verify_access_token(access_token):
    base_url = "https://kapi.kakao.com/v1/user/access_token_info"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    rsp = requests.get(
        base_url,
        headers=headers
    )
    status_code = rsp.status_code
    rsp = rsp.json()
    logger.info(f"return value from kakao: {rsp}")
    
    return rsp, status_code
