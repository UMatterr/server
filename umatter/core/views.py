import logging

from django.shortcuts import render
from django.views.generic.base import TemplateView

from core.utils import auth_user

logger = logging.getLogger('django')

def home(request):
    return render(request, 'home.html')

# @auth_user
# def friends(request):
#     logger.info(f'friends: {request.user}')
#     return render(request, 'friends.html')


class IndexTemplateView(TemplateView):

    template_name = "index.html"
