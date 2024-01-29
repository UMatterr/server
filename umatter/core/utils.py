# ref: https://gist.github.com/josuedjh3/38c521c9091b5c268f2a4d5f3166c497
import logging
import os
import re
import traceback as tb
from functools import wraps
from pathlib import Path

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_list_or_404

from user.models import User
from user.services import get_access_token_by_refresh_token, verify_access_token


logger = logging.getLogger(__name__)

def get_env(key: str, default=None) -> str:
    """
    get environmnet variables
    """
    return os.environ.get(key, default)


class FilePermissionError(Exception):
    """The key file permissions are insecure."""
    pass


def load_env(path: Path):
    """
    >>>
    """
    quote_match = re.compile(r'''[^"]*"(.+)"''').match
    match_setting = re.compile(r'^(?P<name>[A-Z][A-Z_0-9]+)\s?=\s?(?P<value>.*)').match
    aliases = {
        'true': True, 'on': True,
        'false': False, 'off': False
    }

    if not path.exists():
        return

    path = path.resolve()

    if path.stat().st_mode != 0o100600:
        raise FilePermissionError(f"Insecure environment file permissions for {path}! Make it 600")

    content = path.read_text()

    for line in content.split('\n'):
        line = line.strip()

        if not line:
            continue

        if line.startswith('#'):
            continue
        match = match_setting(line)

        if not match:
            continue

        name, value = match.groups()
        quoted = quote_match(value)

        if quoted:
            # Convert 'a', "a" to a, a
            value = str(quoted.groups()[0])

        if name in aliases:
            value = aliases[name]

        # Replace placeholders like ${PATH}
        for match_replace in re.findall(r'(\${([\w\d\-_]+)})', value):
            replace, name = match_replace
            value = value.replace(replace, get_env(name, ''))

        # Set environment value
        os.environ[name] = value


def auth_user(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        access_token = request.COOKIES.get('accessToken')
        refresh_token = request.COOKIES.get('refreshToken')
        logger.info(f"access token: {access_token}")

        if access_token is None \
            or refresh_token is None:
            logger.warning(
                'There is not an access token or a refresh token'
            )
            return HttpResponse(
                'Unauthorized',
                status=401,
            )
        
        try:
            payload, status_code = verify_access_token(access_token)
            logger.info(f"token payload: {status_code}, {payload}")

            if status_code == 401:
                logger.warning(
                    'The access token is expired'
                )
                access_token = get_access_token_by_refresh_token(
                    refresh_token=refresh_token
                )
                payload, status_code = verify_access_token(access_token)
                logger.info(f"reissued token payload: {status_code}, {payload}")

            if status_code != 200:
                raise ValueError(
                    'Something went wrong while verifying access token'
                )

        except:
            logger.error(tb.format_exc())
            return HttpResponse(
                'Unauthorized',
                status=401,
            )

        try:
            logger.info(f"user id: {payload['id']}")
            request.user = get_object_or_404(
                User,
                kakao_id=payload['id']
            )

        except User.DoesNotExist:
            logger.error(tb.format_exc())
            return HttpResponseBadRequest(
                'No user info'
            )
            
        except User.MultipleObjectsReturned:
            logger.error(tb.format_exc())
            return HttpResponseBadRequest(
                'Multiple user info have returned'
            )
            
        except:
            logger.error(tb.format_exc())
            return HttpResponseBadRequest(
                'Something went wrong while getting user info'
            )

        return f(request, *args, **kwargs)

    return wrapper
