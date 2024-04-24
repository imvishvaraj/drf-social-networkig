from django.views.generic.base import RedirectView
from rest_framework.views import APIView
from rest_framework.response import Response


class RootView(RedirectView):
    url = 'https://www.vishvaraj.me'


class StatusView(APIView):
    def get(self, request):
        return Response({"status": "alive"})
