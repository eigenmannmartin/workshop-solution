from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'collections', views.CollectionViewset)
router.register(r'todos', views.TodoViewset)

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.collection, name='collection'),
    path('api/', include(router.urls)),
    path('api/api-auth/', include('rest_framework.urls'))
]
