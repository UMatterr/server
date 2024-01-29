import logging

from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from rest_framework.views import APIView
from rest_framework.response import Response

from core.permissions import KakaoLoginPermission
from .forms import FriendForm
from .models import Friend
from .serializers import FriendSerializer


logger = logging.getLogger(__name__)

# class FriendListView(APIView):
#     permission_classes = [
#         KakaoLoginPermission,
#     ]

#     def get(self, request):
#         friends = Friend.objects.all()
#         serializer = FriendSerializer(friends, many=True)
#         return Response(serializer.data)


class FriendView(ListView, FriendForm):
    permission_classes = [
        KakaoLoginPermission,
    ]
    form_class = FriendForm
    model = Friend
    template_name = 'friends.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super(FriendView, self).get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super(FriendView, self).get(form)
            
