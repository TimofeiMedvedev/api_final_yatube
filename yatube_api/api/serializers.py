from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


from posts.models import Comment, Post, Group, User, Follow


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow

    def validate(self, data):
        user = self.context['request'].user
        following = data['following']
        is_unique = Follow.objects.filter(user=user, following=following)
        if user == following:
            raise serializers.ValidationError(
                'Вы не можете быть подписаны на самого себя.'
            )
        if len(is_unique) != 0:
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора.'
            )
        return data

# class FollowSerializer(serializers.ModelSerializer):
#     user = serializers.SlugRelatedField(
#         queryset=User.objects.all(),
#         slug_field='username',
#         default=serializers.CurrentUserDefault()
#     )

#     following = serializers.SlugRelatedField(
#         queryset=User.objects.all(),
#         slug_field='username'
#     )

#     class Meta:
#         model = Follow
#         fields = '__all__'
#         validators = (
#             UniqueTogetherValidator(
#                 queryset=Follow.objects.all(),
#                 fields=('user', 'following'),
#                 message=('Подписка на Вас уже была оформлена')
#             ),
#         )


#         def validate(self, data):
#             if data['user'] == data['following']:
#                 raise serializers.ValidationError(
#                     'Вы не можете подписаться на самого себя'
#                 )
#             return data