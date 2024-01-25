import logging
import traceback as tb
from functools import wraps

from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
)
from django.shortcuts import get_object_or_404

from .services import verify_access_token
from .models import User
from .services import get_access_token_by_refresh_token


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
            # return HttpResponseRedirect('/auth/login')
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

            