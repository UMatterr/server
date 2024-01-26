import logging

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from user.utils import auth_user

logger = logging.getLogger('django')

def home(request):
    return render(request, 'home.html')

@auth_user
def friends(request):
    logger.info(f'friends: {request.user}')
    return render(request, 'friends.html')


class IndexTemplateView(LoginRequiredMixin, TemplateView):

    template_name = "index.html"
