import json

from django import forms
from django.http import JsonResponse
from django.conf import settings
from django.views import View

from redis_client import redis_client


class ProxyViewForm(forms.Form):
    key = forms.CharField()


class ProxyView(View):
    
    def get(self, request):
        form = ProxyViewForm(request.GET)
        if not form.is_valid():
            return JsonResponse(dict(form.errors), status=400)
        
        key = form.cleaned_data['key']
        key_value = redis_client.get(key)
        if key_value is not None and key_value != settings.KEY_SENTINEL:
            return JsonResponse(json.loads(key_value))
        
        if key_value is None:
            redis_client.set(
                key,
                settings.KEY_SENTINEL,
                settings.CACHE_EXPIRATION,
            )
            redis_client.publish('zvooq_tasks', key)
        
        return JsonResponse({}, status=202)  # 202 Accepted
