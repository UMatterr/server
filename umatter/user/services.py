import logging
import traceback as tb
from urllib.parse import urlencode

from core.utils import get_env
from umatter.settings import BASE_URL

from .models import User


logger = logging.getLogger("user.services")

def get_user_by_kakao_id(kakao_id):
    try:
        user = User.objects.get(kakao_id=kakao_id)
        return user

    except User.DoesNotExist:
        logger.info("Need to create an new user")
        return 1

    except User.MultipleObjectsReturned:
        logger.error("Multiple users with same kakao id")
        return None

    except:
        logger.error(tb.format_exc())
        return None


def create_redirect_uri_for_kakao(base_url:str, params:dict):
    base_params = {
        "client_id": get_env("AUTH_KAKAO_CLIENT_ID"),
        "client_secret": get_env("AUTH_KAKAO_CLIENT_SECRET"),
        "redirect_uri": BASE_URL + get_env("AUTH_KAKAO_REDIRECT_URI_PATH"),
    }
    params = {**base_params, **params}
    params = urlencode(params)
    # logger.info(f"url: {base_url}?{params}")
    return f"{base_url}?{params}"


def create_user_with_kakao_info(
    kakao_id,
    email,
    kakao_nickname,
    profile_thumbnail=None,
):
    user = User.objects.create(
        kakao_id=kakao_id,
        email=email,
        kakao_nickname=kakao_nickname,
        profile_thumbnail=profile_thumbnail,
    )
    logger.info(f"Created user: {user}")
    return user
