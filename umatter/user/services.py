import logging
import os
from urllib.parse import urlencode

from umatter.settings import BASE_URL

from .models import User


logger = logging.getLogger(__name__)

def get_user_by_kakao_token(kakao_token):
    try:
        user = User.objects.get(access_token=kakao_token)
        return user
    except User.DoesNotExist:
        return None
    except User.MultipleObjectsReturned:
        return None
    except:
        return None


def create_redirect_uri_for_kakao(base_url:str, params:dict):
    base_params = {
        "client_id": os.environ.get("AUTH_KAKAO_CLIENT_ID"),
        "client_secret": os.environ.get("AUTH_KAKAO_CLIENT_SECRET"),
        "redirect_uri": BASE_URL + os.environ.get("AUTH_KAKAO_REDIRECT_URI_PATH"),
    }
    params = {**base_params, **params}
    params = urlencode(params)
    # logger.info(f"url: {base_url}?{params}")
    return f"{base_url}?{params}"
