from django.urls import include, path
from rest_framework import routers
from getxerpa.finance.views import UserViewSet,GroupViewSet,CategoryViewSet,TransactionViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'categories', CategoryViewSet,basename='category')
router.register(r'transactions', TransactionViewSet,basename='transaction')


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]