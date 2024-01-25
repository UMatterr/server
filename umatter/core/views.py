import logging
from django.shortcuts import render

from user.utils import auth_user

logger = logging.getLogger('django')

def home(request):
    return render(request, 'index.html')

@auth_user
def friends(request):
    logger.info(f'friends: {request.user}')
    return render(request, 'friends.html')
