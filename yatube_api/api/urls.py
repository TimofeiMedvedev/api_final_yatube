from rest_framework import routers

from django.contrib import admin
from django.urls import include, path

from api.views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('groups', GroupViewSet, basename='groups')
router_v1.register('follow', FollowViewSet, basename='follow')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
# router = routers.DefaultRouter()
# router.register(r'posts', PostViewSet)
# # router.register(r'users', UserViewSet)
# # router.register(r'achievements', AchievementViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
