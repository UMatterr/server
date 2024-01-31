import logging
import traceback as tb

from django.shortcuts import get_object_or_404

from rest_framework import permissions

from user.models import User
from user.services import get_access_token_by_refresh_token, verify_access_token


logger = logging.getLogger(__name__)

class KakaoLoginPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in ('GET', 'POST', 'DELETE'):
            return False

        is_logged_in = request.COOKIES.get('isLoggedIn')
        access_token = request.COOKIES.get('accessToken')
        refresh_token = request.COOKIES.get('refreshToken')
        logger.info(f"is_logged_in: {is_logged_in}, access_token: {access_token}, refresh_token: {refresh_token}", {request.COOKIES})
        if not is_logged_in or is_logged_in is None:
            logger.warning(
                'The user is not logged in'
            )
            return False

        if access_token is None or refresh_token is None:
            logger.warning(
                'There is not an access token or a refresh token'
            )
            return False

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
                logger.error(
                    'Something went wrong while verifying access token'
                )
                return False

        except:
            logger.error(tb.format_exc())
            return False

        try:
            user = get_object_or_404(User, kakao_id=payload['id'])
            logger.info(f"logged in user: {user}")

        except User.DoesNotExist:
            logger.error(tb.format_exc())
            return False

        except User.MultipleObjectsReturned:
            logger.error(tb.format_exc())
            return False

        except:
            logger.error(tb.format_exc())
            return False

        return True
                    
    # def has_object_permission(self, request, view, obj):
    #     if request.method == 'GET':
    #         return True
    #     return False