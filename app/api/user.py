from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers
from rest_framework import generics


# Serializers
class UserSerializer(serializers.HyperlinkedModelSerializer):
    api_key = serializers.Field(source='api_key')
    profile = serializers.Field(source='profile')

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'api_key', 'profile')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    permissions = serializers.ManySlugRelatedField(
        slug_field='codename',
        queryset=Permission.objects.all()
    )

    class Meta:
        model = Group
        fields = ('url', 'name', 'permissions')

# Views


class UserList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of users.
    """
    model = User
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single user.
    """
    model = User
    serializer_class = UserSerializer


class GroupList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of groups.
    """
    model = Group
    serializer_class = GroupSerializer


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single group.
    """
    model = Group
    serializer_class = GroupSerializer
