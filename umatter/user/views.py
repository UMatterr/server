import logging
import requests
import traceback as tb

from core.utils import get_env
from django.http import (
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect

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
from .utils import auth_user
from umatter.settings import BASE_URL

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework import status


logger = logging.getLogger("user.views")

def kakao_login(request):

    # if bool(request.COOKIES.get("isLoggedIn")):
    #     logger.info(f"COOKIE: {request.COOKIES}")
    #     logger.info("already logged in")
    #     return redirect('/')

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


# class RegisterAPIView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
            
#             # jwt 토큰 접근
#             token = TokenObtainPairSerializer.get_token(user)
#             refresh_token = str(token)
#             access_token = str(token.access_token)
#             res = Response(
#                 {
#                     "user": serializer.data,
#                     "message": "register successs",
#                     "token": {
#                         "access": access_token,
#                         "refresh": refresh_token,
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )
            
#             # jwt 토큰 => 쿠키에 저장
#             res.set_cookie("access", access_token, httponly=True)
#             res.set_cookie("refresh", refresh_token, httponly=True)
            
#             return res

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


# class AuthAPIView(APIView):
#     # 유저 정보 확인
#     def get(self, request):
#         try:
#             # access token을 decode 해서 유저 id 추출 => 유저 식별
#             access = request.COOKIES['access']
#             payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
#             pk = payload.get('user_id')
#             user = get_object_or_404(User, pk=pk)
#             serializer = UserSerializer(instance=user)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except(jwt.exceptions.ExpiredSignatureError):
#             # 토큰 만료 시 토큰 갱신
#             data = {'refresh': request.COOKIES.get('refresh', None)}
#             serializer = TokenRefreshSerializer(data=data)
#             if serializer.is_valid(raise_exception=True):
#                 access = serializer.data.get('access', None)
#                 refresh = serializer.data.get('refresh', None)
#                 payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
#                 pk = payload.get('user_id')
#                 user = get_object_or_404(User, pk=pk)
#                 serializer = UserSerializer(instance=user)
#                 res = Response(serializer.data, status=status.HTTP_200_OK)
#                 res.set_cookie('access', access)
#                 res.set_cookie('refresh', refresh)
#                 return res
#             raise jwt.exceptions.InvalidTokenError

#         except(jwt.exceptions.InvalidTokenError):
#             # 사용 불가능한 토큰일 때
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     # 로그인
#     def post(self, request):
#     	# 유저 인증
#         user = authenticate(
#             email=request.data.get("email"), password=request.data.get("password")
#         )
#         # 이미 회원가입 된 유저일 때
#         if user is not None:
#             serializer = UserSerializer(user)
#             # jwt 토큰 접근
#             token = TokenObtainPairSerializer.get_token(user)
#             refresh_token = str(token)
#             access_token = str(token.access_token)
#             res = Response(
#                 {
#                     "user": serializer.data,
#                     "message": "login success",
#                     "token": {
#                         "access": access_token,
#                         "refresh": refresh_token,
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )
#             # jwt 토큰 => 쿠키에 저장
#             res.set_cookie("access", access_token, httponly=True)
#             res.set_cookie("refresh", refresh_token, httponly=True)
#             return res
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     # 로그아웃
#     def delete(self, request):
#         # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
#         response = Response({
#             "message": "Logout success"
#             }, status=status.HTTP_202_ACCEPTED)
#         response.delete_cookie("access")
#         response.delete_cookie("refresh")
#         return response
