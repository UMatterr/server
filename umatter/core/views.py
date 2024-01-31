import logging

from django.shortcuts import render
from django.views.generic.base import TemplateView

# from user.utils import auth_user

logger = logging.getLogger('django')

class IndexTemplateView(TemplateView):

    template_name = "index.html"
