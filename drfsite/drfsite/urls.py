"""
URL configuration for drfsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from queuetask.views import QueueEntryViewSet, OperationsViewSet
from django.contrib import admin

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

router = DefaultRouter()
router.register(r'queue', QueueEntryViewSet, basename='queue')
#router.register(r'operations', OperationsViewSet, basename='operations')



urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path(
        'api/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'api/schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),

    path('admin/', admin.site.urls),
    path('operations/create/', OperationsViewSet.as_view({'post': 'export_data'}), name='export-data'),
    path('operations/tt/<uuid:operation_id>/', OperationsViewSet.as_view({'get': 'retrieve'}), name='get-operation'),
    path('operations/report/<path:filename>/', OperationsViewSet.as_view({'get': 'download_file'}), name='download-file'),

    path('queue/', QueueEntryViewSet.as_view({'post': 'create'}), name='create-queue'),
    path('queue/<int:queue_id>/', QueueEntryViewSet.as_view({'get': 'get_queue'}), name='list-of-users'),
    path('queue/add_user/<int:queue_id>/<int:user_id>/', QueueEntryViewSet.as_view({'get': 'add_user_to_queue'}), name='add-user-to-queue'),
    path('queue/change_st/notifyed/<int:queue_id>/<int:user_id>/', QueueEntryViewSet.as_view({'get': 'notify'}), name='change-st-notifyed'),
    path('queue/change_st/served/<int:queue_id>/<int:user_id>/', QueueEntryViewSet.as_view({'get': 'serve'}), name='change-st-served'),
] + router.urls


