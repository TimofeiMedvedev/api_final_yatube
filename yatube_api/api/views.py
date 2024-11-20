from rest_framework import viewsets
from django.shortcuts import get_object_or_404
# from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from posts.models import Post, Comment, Group
from .serializers import PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
from api.permissions import IsAuthorOrReadOnlyPermission
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination

class ListCreateViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    pass

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            return (IsAuthenticated(),)
        return super().get_permissions()

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    # def perform_create(self, serializer):
    #     post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
    #     serializer.save(author=self.request.user, post=post)

    # def get_queryset(self):
    #     post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
    #     return post.comments.all()
    
    # def get_permissions(self):
    #     if self.action == 'create':
    #         return (IsAuthenticated(),)
    #     return super().get_permissions()

    def get_post(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())

    def get_queryset(self):
        return self.get_post().comments.all()
    
    def get_permissions(self):
        if self.action == 'create':
            return (IsAuthenticated(),)
        return super().get_permissions()
    
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

class FollowViewSet(ListCreateViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    pagination_class = None

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


