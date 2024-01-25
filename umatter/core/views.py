import logging
from django.shortcuts import render

from user.utils import auth_user

logger = logging.getLogger('django')

def home(request):
    return render(request, 'index.html')

@auth_user
def test_friend(request):
    logger.info(f'test_friend: {request.user}')
    return render(request, 'friends.html')
