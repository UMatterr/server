import logging

from django.http import HttpResponse
from django.views.generic.base import TemplateView

logger = logging.getLogger('django')

class IndexTemplateView(TemplateView):

    template_name = "index.html"


def health_check(request):
    return HttpResponse("OK")
