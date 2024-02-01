import logging
import traceback as tb
from functools import wraps

from django.http import (
    HttpResponse, HttpResponseBadRequest,
    HttpResponseNotAllowed, HttpResponseNotFound,
)

from .models import User
from .services import get_access_token_by_refresh_token, verify_access_token


logger = logging.getLogger(__name__)

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
            logger.error(f'ERROR: {tb.format_exc()}')
            return HttpResponse(
                'Unauthorized',
                status=401,
            )

        try:
            logger.info(f"user kakao id: {payload['id']}")
            user_info = User.objects.get(
                kakao_id=payload['id']
            )
            request.user = user_info
            logger.info(f"user kakao id: {type(user_info)}")

        except User.DoesNotExist:
            logger.error(tb.format_exc())
            return HttpResponseNotFound(
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


def control_request_method(method=('GET')):
    def wrapper(func):
        def _inner(request, *args, **kwargs):
            logger.info(
                "request method: %s, %s",
                request.method, method
            )
            if request.method not in method:
                return HttpResponseNotAllowed(method)
            return func(request, *args, **kwargs)
        return _inner
    return wrapper
