from django.conf.urls import url, include
from rest_framework import routers

from saver import views


router = routers.SimpleRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'data', views.DataViewSet)
urlpatterns = router.urls

urlpatterns = [
    url(r'^', include(router.urls)),
    url('^clients/name/(?P<name>.+)/$', views.ClientViewName.as_view())
]
