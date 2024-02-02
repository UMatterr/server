import logging

from django.shortcuts import render
from django.views.generic.base import TemplateView

logger = logging.getLogger('django')

class IndexTemplateView(TemplateView):

    template_name = "index.html"
