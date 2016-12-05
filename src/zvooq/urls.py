
from django.conf.urls import url
from request_proxy.views import ProxyView

urlpatterns = [
    url(r'^from_cache$', ProxyView.as_view(), name='request_proxy'),
]
